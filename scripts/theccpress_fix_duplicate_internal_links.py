#!/usr/bin/env python3

import csv
import os
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse

import requests


BASE = "https://theccpress.com"
ROOT = Path("/home/qcweb/rewrite-and-improve")
MAPPING_FILE = ROOT / "theccpress_duplicate_internal_link_fix_summary_2026-06-11.csv"
DRYRUN_FILE = ROOT / "theccpress_duplicate_internal_link_fix_live_scan_2026-06-14.csv"
RESULT_FILE = ROOT / "theccpress_duplicate_internal_link_fix_live_updates_2026-06-14.csv"
SUMMARY_FILE = ROOT / "theccpress_duplicate_internal_link_fix_live_updates_2026-06-14.md"
API_ROOT = f"{BASE}/wp-json/wp/v2/posts"
USER_AGENT = "Mozilla/5.0 (compatible; QCWebAudit/1.0; +https://theccpress.com)"


def load_mappings() -> List[Dict[str, str]]:
    mappings: List[Dict[str, str]] = []
    seen = set()

    with MAPPING_FILE.open(newline="") as f:
        for row in csv.DictReader(f):
            old_url = row["old_url"].strip()
            new_url = row["new_url"].strip()
            if not old_url or not new_url:
                continue
            key = (old_url, new_url)
            if key in seen:
                continue
            seen.add(key)
            mappings.append(
                {
                    "old_rel": old_url,
                    "old_abs": f"{BASE}{old_url}",
                    "new_abs": new_url,
                    "new_rel": urlparse(new_url).path,
                }
            )

    return mappings


def get_session() -> requests.Session:
    user = os.environ["WP_USER"]
    app_pass = os.environ["WP_APP_PASS"]
    session = requests.Session()
    session.auth = (user, app_pass)
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def iter_published_posts(session: requests.Session) -> List[Dict]:
    posts: List[Dict] = []
    page = 1

    while True:
        response = session.get(
            API_ROOT,
            params={
                "status": "publish",
                "context": "edit",
                "per_page": 100,
                "page": page,
                "_fields": "id,slug,link,status,title,content",
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        posts.extend(data)

        total_pages = int(response.headers.get("X-WP-TotalPages", "1"))
        print(f"fetched posts page {page}/{total_pages}", flush=True)
        if page >= total_pages:
            break
        page += 1

    return posts


def replace_links(content: str, mappings: List[Dict[str, str]]) -> Dict[str, object]:
    updated = content
    matched = []

    for mapping in mappings:
        count = 0
        if mapping["old_abs"] in updated:
            c = updated.count(mapping["old_abs"])
            updated = updated.replace(mapping["old_abs"], mapping["new_abs"])
            count += c
        if mapping["old_rel"] in updated:
            c = updated.count(mapping["old_rel"])
            updated = updated.replace(mapping["old_rel"], mapping["new_rel"])
            count += c
        if count:
            matched.append(
                {
                    "old_rel": mapping["old_rel"],
                    "new_rel": mapping["new_rel"],
                    "replacements": count,
                }
            )

    return {
        "changed": updated != content,
        "content": updated,
        "matches": matched,
    }


def write_scan(scan_rows: List[Dict[str, object]]) -> None:
    with DRYRUN_FILE.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "post_id",
                "post_url",
                "post_slug",
                "matches",
                "replacement_count",
                "old_urls",
            ]
        )
        for row in scan_rows:
            writer.writerow(
                [
                    row["post_id"],
                    row["post_url"],
                    row["post_slug"],
                    len(row["matches"]),
                    row["replacement_count"],
                    " | ".join(match["old_rel"] for match in row["matches"]),
                ]
            )


def write_results(result_rows: List[Dict[str, object]], total_posts: int, changed_posts: int) -> None:
    with RESULT_FILE.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "post_id",
                "post_url",
                "post_slug",
                "status",
                "replacement_count",
                "old_urls",
            ]
        )
        for row in result_rows:
            writer.writerow(
                [
                    row["post_id"],
                    row["post_url"],
                    row["post_slug"],
                    row["status"],
                    row["replacement_count"],
                    " | ".join(match["old_rel"] for match in row["matches"]),
                ]
            )

    with SUMMARY_FILE.open("w") as f:
        f.write("# TheCCPress Duplicate Internal Link Live Update\n\n")
        f.write("Date: 2026-06-14\n\n")
        f.write(f"- published posts scanned: `{total_posts}`\n")
        f.write(f"- published posts updated: `{changed_posts}`\n")
        f.write(f"- detailed scan: `{DRYRUN_FILE}`\n")
        f.write(f"- detailed update log: `{RESULT_FILE}`\n\n")

        if result_rows:
            f.write("## Updated Posts\n\n")
            for row in result_rows:
                f.write(
                    f"- `{row['post_url']}` | replacements `{row['replacement_count']}` | "
                    f"status `{row['status']}`\n"
                )


def main() -> None:
    mappings = load_mappings()
    session = get_session()
    dry_run = os.environ.get("DRY_RUN", "0") == "1"
    posts = iter_published_posts(session)

    scan_rows: List[Dict[str, object]] = []
    changed_posts = []

    for idx, post in enumerate(posts, 1):
        raw_content = post["content"]["raw"]
        replacement = replace_links(raw_content, mappings)
        if replacement["changed"]:
            changed_posts.append(
                {
                    "post_id": post["id"],
                    "post_url": post["link"],
                    "post_slug": post["slug"],
                    "content": replacement["content"],
                    "matches": replacement["matches"],
                    "replacement_count": sum(m["replacements"] for m in replacement["matches"]),
                }
            )
        if replacement["matches"]:
            scan_rows.append(
                {
                    "post_id": post["id"],
                    "post_url": post["link"],
                    "post_slug": post["slug"],
                    "matches": replacement["matches"],
                    "replacement_count": sum(m["replacements"] for m in replacement["matches"]),
                }
            )
        if idx % 100 == 0:
            print(f"scanned {idx}/{len(posts)} published posts", flush=True)

    write_scan(scan_rows)

    result_rows = []
    for idx, row in enumerate(changed_posts, 1):
        if dry_run:
            status = "dry_run"
        else:
            response = session.post(
                f"{API_ROOT}/{row['post_id']}",
                json={"content": row["content"]},
                timeout=30,
            )
            status = "updated" if response.ok else f"error_{response.status_code}"
            if not response.ok:
                try:
                    status = f"{status}:{response.json().get('message', '')}"
                except Exception:  # noqa: BLE001
                    pass
        result_rows.append(
            {
                "post_id": row["post_id"],
                "post_url": row["post_url"],
                "post_slug": row["post_slug"],
                "status": status,
                "replacement_count": row["replacement_count"],
                "matches": row["matches"],
            }
        )
        print(f"updated {idx}/{len(changed_posts)} -> {row['post_slug']} [{status}]", flush=True)

    write_results(result_rows, len(posts), len(changed_posts))

    print("done")
    print(f"published_posts {len(posts)}")
    print(f"changed_posts {len(changed_posts)}")
    print(f"dry_run {dry_run}")
    print(DRYRUN_FILE)
    print(RESULT_FILE)
    print(SUMMARY_FILE)


if __name__ == "__main__":
    main()
