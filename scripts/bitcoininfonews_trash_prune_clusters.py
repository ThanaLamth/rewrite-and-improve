from __future__ import annotations

import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth


ROOT = Path("/home/qcweb/rewrite-and-improve")
INPUT_PATH = ROOT / "bitcoininfonews_action_prune_now_content_2026-06-09.csv"
DATE_STAMP = "2026-06-09"

WP_BASE = "https://bitcoininfonews.com/wp-json/wp/v2/posts"
AUTH = HTTPBasicAuth("Diego Martinez", "Uo1P KG5l kLnW ghIj 3qPP YuFh")
HEADERS = {"User-Agent": "Mozilla/5.0 (Codex prune cluster trash worker)"}

TARGET_CLUSTERS = {
    "BlockDAG": "brand_blockdag",
    "Cold Wallet": "brand_cold_wallet",
    "Qubetics": "brand_qubetics",
    "Web3 ai": "brand_web3_ai",
    "Unstaked": "brand_unstaked",
    "BTFD": "brand_btfd",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    return path.split("/")[-1]


def cluster_name(row: dict[str, str]) -> str:
    rules = set(row["matched_rule"].split("|"))
    for label, key in TARGET_CLUSTERS.items():
        if key in rules:
            return label
    return "Other"


def fetch_post(row: dict[str, str]) -> dict[str, object]:
    slug = slug_from_url(row["url"])
    params = {
        "slug": slug,
        "_fields": "id,slug,link,status,date,title",
        "per_page": 100,
    }
    result: dict[str, object] = {
        "cluster": cluster_name(row),
        "url": row["url"],
        "slug": slug,
        "title": row["title"],
        "matched_rule": row["matched_rule"],
        "gsc_clicks": row["gsc_clicks"],
        "gsc_impressions": row["gsc_impressions"],
    }
    try:
        resp = requests.get(WP_BASE, params=params, auth=AUTH, headers=HEADERS, timeout=30)
        result["lookup_status"] = resp.status_code
        if resp.status_code != 200:
            result["lookup_result"] = "lookup_http_error"
            result["lookup_note"] = resp.text[:300]
            return result
        items = resp.json()
        exact = None
        for item in items:
            if item.get("link", "").rstrip("/") == row["url"].rstrip("/"):
                exact = item
                break
        if exact is None and items:
            exact = items[0]
        if exact is None:
            result["lookup_result"] = "not_found"
            result["lookup_note"] = ""
            return result
        result["post_id"] = exact.get("id", "")
        result["post_status"] = exact.get("status", "")
        result["post_date"] = exact.get("date", "")
        result["post_link"] = exact.get("link", "")
        result["lookup_result"] = "found"
        result["lookup_note"] = ""
        return result
    except Exception as exc:  # noqa: BLE001
        result["lookup_status"] = "ERR"
        result["lookup_result"] = "lookup_exception"
        result["lookup_note"] = str(exc)
        return result


def trash_post(lookup_row: dict[str, object]) -> dict[str, object]:
    result = dict(lookup_row)
    post_id = lookup_row.get("post_id")
    if not post_id:
        result["trash_result"] = "skipped_no_post_id"
        result["trash_status"] = ""
        result["trash_note"] = ""
        return result
    try:
        resp = requests.delete(
            f"{WP_BASE}/{post_id}",
            params={"force": "false"},
            auth=AUTH,
            headers=HEADERS,
            timeout=30,
        )
        result["trash_status"] = resp.status_code
        if resp.status_code not in {200, 202}:
            result["trash_result"] = "trash_http_error"
            result["trash_note"] = resp.text[:300]
            return result
        payload = resp.json()
        result["trash_result"] = "trashed" if payload.get("status") == "trash" else "unexpected_status"
        result["trash_note"] = payload.get("status", "")
        return result
    except Exception as exc:  # noqa: BLE001
        result["trash_status"] = "ERR"
        result["trash_result"] = "trash_exception"
        result["trash_note"] = str(exc)
        return result


def main() -> None:
    rows = read_csv(INPUT_PATH)
    targets = [row for row in rows if cluster_name(row) in TARGET_CLUSTERS]

    lookup_rows: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_post, row) for row in targets]
        for future in as_completed(futures):
            lookup_rows.append(future.result())

    lookup_rows.sort(key=lambda row: (str(row["cluster"]), str(row["url"])))

    manifest_path = ROOT / f"bitcoininfonews_prune_cluster_manifest_{DATE_STAMP}.csv"
    manifest_fields = [
        "cluster",
        "url",
        "slug",
        "title",
        "matched_rule",
        "gsc_clicks",
        "gsc_impressions",
        "lookup_status",
        "lookup_result",
        "lookup_note",
        "post_id",
        "post_status",
        "post_date",
        "post_link",
    ]
    write_csv(manifest_path, lookup_rows, manifest_fields)

    found_rows = [row for row in lookup_rows if row.get("lookup_result") == "found"]
    trashed_rows: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(trash_post, row) for row in found_rows]
        for future in as_completed(futures):
            trashed_rows.append(future.result())

    missing_rows = [row for row in lookup_rows if row.get("lookup_result") != "found"]
    all_results = trashed_rows + missing_rows
    all_results.sort(key=lambda row: (str(row["cluster"]), str(row["url"])))

    result_path = ROOT / f"bitcoininfonews_prune_cluster_trash_results_{DATE_STAMP}.csv"
    result_fields = manifest_fields + ["trash_status", "trash_result", "trash_note"]
    write_csv(result_path, all_results, result_fields)

    summary_path = ROOT / f"bitcoininfonews_prune_cluster_trash_summary_{DATE_STAMP}.md"
    counts: dict[str, int] = {}
    for row in all_results:
        key = str(row.get("trash_result") or row.get("lookup_result"))
        counts[key] = counts.get(key, 0) + 1

    cluster_counts: dict[str, int] = {}
    for row in all_results:
        if row.get("trash_result") == "trashed":
            key = str(row["cluster"])
            cluster_counts[key] = cluster_counts.get(key, 0) + 1

    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write("# BitcoinInfoNews prune cluster trash summary\n\n")
        fh.write(f"- Target URLs: {len(targets)}\n")
        fh.write(f"- Found via REST: {len(found_rows)}\n")
        fh.write(f"- Missing via REST: {len(missing_rows)}\n\n")
        fh.write("## Result counts\n\n")
        for key, value in sorted(counts.items()):
            fh.write(f"- {key}: {value}\n")
        fh.write("\n## Trashed by cluster\n\n")
        for key, value in sorted(cluster_counts.items()):
            fh.write(f"- {key}: {value}\n")

    print(manifest_path)
    print(result_path)
    print(summary_path)


if __name__ == "__main__":
    main()
