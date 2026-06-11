#!/usr/bin/env python3

import csv
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse


INPUT_CSV = Path("/home/qcweb/ccpress 2nd/internal_all.csv")
OUTPUT_DIR = Path("/home/qcweb/rewrite-and-improve")

OUTPUT_DECISION = OUTPUT_DIR / "theccpress_duplicate_cluster_decision_sheet_2026-06-11.csv"
OUTPUT_SAFE_IMPORT = OUTPUT_DIR / "theccpress_duplicate_301_safe_import_2026-06-11.csv"
OUTPUT_TIER1_IMPORT = OUTPUT_DIR / "theccpress_duplicate_301_tier1_review_import_2026-06-11.csv"
OUTPUT_FULL_IMPORT = OUTPUT_DIR / "theccpress_duplicate_301_full_import_2026-06-11.csv"
OUTPUT_RANKMATH_IMPORT = OUTPUT_DIR / "theccpress_duplicate_301_rankmath_import_2026-06-11.csv"

SUFFIX_RE = re.compile(r"-(\d+)/?$")

MANUAL_KEEPERS = {
    "Arizona Governor Vetoes Bitcoin Reserve Bill": "https://theccpress.com/arizona-bitcoin-reserve-bill-veto/",
    "REX Shares Files for Ethereum and Solana Staking ETFs": "https://theccpress.com/rex-ethereum-solana-staking-etfs/",
    "REX Shares Files for Ethereum, Solana Staking ETFs": "https://theccpress.com/rex-shares-ethereum-solana-etfs/",
    "SEC Approves In-Kind Redemptions for Bitcoin, Ethereum ETFs": "https://theccpress.com/sec-approves-in-kind-redemptions-etfs/",
}


def to_int(value: str) -> int:
    value = (value or "").strip()
    if not value:
        return 0
    try:
        return int(float(value))
    except ValueError:
        return 0


def is_indexable_html(row: dict[str, str]) -> bool:
    return (
        row.get("Status Code") == "200"
        and row.get("Indexability") == "Indexable"
        and row.get("Content Type", "").startswith("text/html")
    )


def is_suffix_url(url: str) -> bool:
    return bool(SUFFIX_RE.search(url))


def path_only(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    return path if path.endswith("/") else f"{path}/"


def absolute_url(url: str) -> str:
    return f"https://theccpress.com{path_only(url)}"


def choose_heuristic_keeper(rows: list[dict[str, str]]) -> str:
    def sort_key(row: dict[str, str]) -> tuple[int, int, int, str]:
        url = row["Address"]
        return (
            to_int(row.get("Unique Inlinks", "")),
            0 if is_suffix_url(url) else 1,
            -len(path_only(url)),
            url,
        )

    return max(rows, key=sort_key)["Address"]


def load_clusters() -> dict[str, list[dict[str, str]]]:
    clusters: dict[str, list[dict[str, str]]] = defaultdict(list)
    with INPUT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if not is_indexable_html(row):
                continue
            title = (row.get("Title 1") or "").strip()
            if not title:
                continue
            clusters[title].append(row)
    return {title: rows for title, rows in clusters.items() if len(rows) > 1}


def main() -> None:
    clusters = load_clusters()

    decision_rows: list[dict[str, str]] = []
    safe_import_rows: list[list[str]] = []
    tier1_import_rows: list[list[str]] = []
    full_import_rows: list[list[str]] = []

    for title, rows in sorted(clusters.items(), key=lambda item: (-len(item[1]), item[0].lower())):
        rows_sorted = sorted(rows, key=lambda row: row["Address"])
        base_rows = [row for row in rows_sorted if not is_suffix_url(row["Address"])]
        suffix_rows = [row for row in rows_sorted if is_suffix_url(row["Address"])]

        keeper = MANUAL_KEEPERS.get(title) or choose_heuristic_keeper(rows_sorted)
        cluster_type = "exact_title_duplicate"
        if suffix_rows:
            cluster_type = "exact_title_duplicate_with_suffix"

        if title in MANUAL_KEEPERS:
            default_action = "review_301"
            confidence = "medium"
            reason = "major duplicate cluster from audit; keeper chosen manually"
        elif len(base_rows) == 1 and suffix_rows:
            default_action = "301_now"
            confidence = "high"
            reason = "exact duplicate title with one clean base URL and suffix duplicate"
        else:
            default_action = "review_301"
            confidence = "medium"
            reason = "exact duplicate title but keeper still needs human confirmation"

        for row in rows_sorted:
            url = row["Address"]
            if url == keeper:
                action = "keep"
                row_reason = "preferred keeper for this duplicate cluster"
            else:
                action = default_action
                row_reason = reason

                if action == "301_now":
                    safe_import_rows.append([path_only(url), path_only(keeper)])
                elif title in MANUAL_KEEPERS:
                    tier1_import_rows.append([path_only(url), path_only(keeper)])

                full_import_rows.append([path_only(url), path_only(keeper)])

            decision_rows.append(
                {
                    "cluster_title": title,
                    "cluster_size": str(len(rows_sorted)),
                    "cluster_type": cluster_type,
                    "url": url,
                    "path": path_only(url),
                    "unique_inlinks": row.get("Unique Inlinks", ""),
                    "word_count": row.get("Word Count", ""),
                    "keeper_url": keeper,
                    "keeper_path": path_only(keeper),
                    "recommended_action": action,
                    "confidence": "high" if action == "301_now" else confidence if action != "keep" else "high",
                    "note": row_reason,
                }
            )

    with OUTPUT_DECISION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "cluster_title",
                "cluster_size",
                "cluster_type",
                "url",
                "path",
                "unique_inlinks",
                "word_count",
                "keeper_url",
                "keeper_path",
                "recommended_action",
                "confidence",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(decision_rows)

    with OUTPUT_SAFE_IMPORT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source URL", "target URL"])
        writer.writerows(sorted(set(tuple(row) for row in safe_import_rows)))

    with OUTPUT_TIER1_IMPORT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source URL", "target URL"])
        writer.writerows(sorted(set(tuple(row) for row in tier1_import_rows)))

    with OUTPUT_FULL_IMPORT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source URL", "target URL"])
        writer.writerows(sorted(set(tuple(row) for row in full_import_rows)))

    with OUTPUT_RANKMATH_IMPORT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "source",
                "matching",
                "destination",
                "type",
                "category",
                "status",
                "ignore",
            ],
        )
        writer.writeheader()
        for source, destination in sorted(set(tuple(row) for row in full_import_rows)):
            writer.writerow(
                {
                    "id": "",
                    "source": source,
                    "matching": "exact",
                    "destination": absolute_url(destination),
                    "type": "301",
                    "category": "theccpress_duplicate_batch_1",
                    "status": "active",
                    "ignore": "",
                }
            )

    print(f"decision_rows={len(decision_rows)}")
    print(f"safe_import_rows={len(set(tuple(row) for row in safe_import_rows))}")
    print(f"tier1_import_rows={len(set(tuple(row) for row in tier1_import_rows))}")
    print(f"full_import_rows={len(set(tuple(row) for row in full_import_rows))}")
    print(OUTPUT_DECISION)
    print(OUTPUT_SAFE_IMPORT)
    print(OUTPUT_TIER1_IMPORT)
    print(OUTPUT_FULL_IMPORT)
    print(OUTPUT_RANKMATH_IMPORT)


if __name__ == "__main__":
    main()
