#!/usr/bin/env python3

import csv
from pathlib import Path
from urllib.parse import urljoin

import requests


BASE = "https://theccpress.com"
ROOT = Path("/home/qcweb/rewrite-and-improve")
INFILE = ROOT / "theccpress_redirection_pending_bulk_2026-06-09.csv"
OUTFILE = ROOT / "theccpress_redirection_pending_bulk_missing_2026-06-14.csv"
PLUGIN_OUTFILE = ROOT / "theccpress_redirection_pending_bulk_missing_plugin_2026-06-14.csv"
SUMMARY = ROOT / "theccpress_redirection_pending_bulk_missing_2026-06-14.md"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; QCWebAudit/1.0; +https://theccpress.com)"
}


def main() -> None:
    session = requests.Session()
    rows = []

    with INFILE.open(newline="") as f:
        for source, target, regex, code in csv.reader(f):
            rows.append(
                {
                    "source": source,
                    "target": target,
                    "regex": regex,
                    "code": code,
                }
            )

    results = []
    for idx, row in enumerate(rows, 1):
        src = urljoin(BASE, row["source"])
        tgt = urljoin(BASE, row["target"])

        try:
            src_resp = session.get(src, headers=HEADERS, allow_redirects=False, timeout=20)
            src_status = src_resp.status_code
            src_location = src_resp.headers.get("Location", "")
        except Exception as exc:  # noqa: BLE001
            src_status = "ERR"
            src_location = str(exc)

        try:
            tgt_resp = session.get(tgt, headers=HEADERS, allow_redirects=False, timeout=20)
            tgt_status = tgt_resp.status_code
        except Exception:  # noqa: BLE001
            tgt_status = "ERR"

        row["src_status"] = src_status
        row["src_location"] = src_location
        row["tgt_status"] = tgt_status
        results.append(row)

        if idx % 10 == 0:
            print(f"checked {idx}/{len(rows)}", flush=True)

    missing = []
    already_ok = []
    needs_review = []

    for row in results:
        desired = urljoin(BASE, row["target"]).rstrip("/")
        current = (
            urljoin(BASE, row["src_location"]).rstrip("/") if row["src_location"] else ""
        )

        if row["tgt_status"] != 200:
            needs_review.append((row, "target_not_200"))
        elif row["src_status"] in (301, 302, 307, 308) and current == desired:
            already_ok.append(row)
        else:
            missing.append(row)

    with OUTFILE.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "destination", "matching", "type"])
        for row in missing:
            writer.writerow([row["source"], row["target"], "url", row["code"]])

    with PLUGIN_OUTFILE.open("w", newline="") as f:
        writer = csv.writer(f)
        for row in missing:
            writer.writerow([row["source"], row["target"], "0", row["code"]])

    with SUMMARY.open("w") as f:
        f.write("# TheCCPress Pending 301 Batch Recheck\n\n")
        f.write("Date: 2026-06-14\n\n")
        f.write(f"- input rows: `{len(results)}`\n")
        f.write(f"- already redirecting correctly: `{len(already_ok)}`\n")
        f.write(f"- still missing and should be imported: `{len(missing)}`\n")
        f.write(f"- needs review because target is not 200: `{len(needs_review)}`\n\n")

        if missing:
            f.write("## Missing Redirects\n\n")
            for row in missing:
                location = row["src_location"] if row["src_location"] else "-"
                f.write(
                    f"- `{row['source']}` -> `{row['target']}` | "
                    f"source status `{row['src_status']}` | "
                    f"location `{location}`\n"
                )
            f.write("\n")

        if already_ok:
            f.write("## Already OK\n\n")
            for row in already_ok:
                f.write(f"- `{row['source']}` -> `{row['target']}`\n")
            f.write("\n")

        if needs_review:
            f.write("## Needs Review\n\n")
            for row, reason in needs_review:
                f.write(
                    f"- `{row['source']}` -> `{row['target']}` | "
                    f"target status `{row['tgt_status']}` | "
                    f"reason `{reason}`\n"
                )

    print("done")
    print(f"results {len(results)}")
    print(f"already_ok {len(already_ok)}")
    print(f"missing {len(missing)}")
    print(f"needs_review {len(needs_review)}")
    print(OUTFILE)
    print(PLUGIN_OUTFILE)
    print(SUMMARY)


if __name__ == "__main__":
    main()
