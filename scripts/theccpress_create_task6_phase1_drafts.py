#!/usr/bin/env python3

import csv
import os
from pathlib import Path

import requests


ROOT = Path("/home/qcweb/rewrite-and-improve")
BUILD_SHEET = ROOT / "theccpress_task6_phase1_build_sheet_2026-06-14.csv"
RESULT_FILE = ROOT / "theccpress_task6_phase1_draft_create_results_2026-06-14.csv"
SUMMARY_FILE = ROOT / "theccpress_task6_phase1_draft_create_results_2026-06-14.md"
API = "https://theccpress.com/wp-json/wp/v2/pages"
USER_AGENT = "Mozilla/5.0 (compatible; QCWebAudit/1.0; +https://theccpress.com)"


def build_content(row: dict) -> str:
    title = row["title"]
    parent_hub = row["parent_hub"]
    primary_intent = row["primary_intent"]
    secondary_intent = row["secondary_intent"]
    top_sources = row["top_internal_sources"].split(" ; ")
    bullets = "\n".join(f"<li>{src}</li>" for src in top_sources)
    return f"""
<!-- wp:paragraph -->
<p><strong>Draft purpose:</strong> evergreen landing page for {primary_intent} intent with secondary support for {secondary_intent}.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Recommended Angle</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>This draft should become a durable non-brand landing page under the hub <a href="{parent_hub}">{parent_hub}</a>. It should explain the concept clearly for beginners, then route readers to the next logical action.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Suggested Outline</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>Definition and plain-English explanation</li>
<li>Why it matters in crypto</li>
<li>How it works in practice</li>
<li>Main risks or mistakes</li>
<li>Beginner-friendly examples</li>
<li>Related guides to link next</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Planned Internal Sources</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
{bullets}
</ul>
<!-- /wp:list -->
""".strip()


def main() -> None:
    user = os.environ["WP_USER"]
    app_pass = os.environ["WP_APP_PASS"]
    session = requests.Session()
    session.auth = (user, app_pass)
    session.headers.update({"User-Agent": USER_AGENT})

    rows = []
    with BUILD_SHEET.open(newline="") as f:
        rows = list(csv.DictReader(f))

    results = []
    for row in rows:
        payload = {
            "title": row["title"],
            "slug": row["slug"],
            "status": "draft",
            "content": build_content(row),
        }
        response = session.post(API, json=payload, timeout=30)
        status = "created" if response.ok else f"error_{response.status_code}"
        page_id = ""
        link = ""
        if response.ok:
            data = response.json()
            page_id = data.get("id", "")
            link = data.get("link", "")
        else:
            try:
                status = f"{status}:{response.json().get('message', '')}"
            except Exception:  # noqa: BLE001
                pass
        results.append(
            {
                "slug": row["slug"],
                "title": row["title"],
                "status": status,
                "page_id": page_id,
                "link": link,
            }
        )
        print(f"{row['slug']} -> {status}", flush=True)

    with RESULT_FILE.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["slug", "title", "status", "page_id", "link"])
        for row in results:
            writer.writerow([row["slug"], row["title"], row["status"], row["page_id"], row["link"]])

    created = [r for r in results if r["status"] == "created"]
    with SUMMARY_FILE.open("w") as f:
        f.write("# TheCCPress Task 6 Phase 1 Draft Creation\n\n")
        f.write("Date: 2026-06-14\n\n")
        f.write(f"- requested drafts: `{len(results)}`\n")
        f.write(f"- created drafts: `{len(created)}`\n")
        f.write(f"- result log: `{RESULT_FILE}`\n\n")
        if created:
            f.write("## Created Drafts\n\n")
            for row in created:
                f.write(f"- `{row['slug']}` | id `{row['page_id']}` | `{row['link']}`\n")

    print(RESULT_FILE)
    print(SUMMARY_FILE)


if __name__ == "__main__":
    main()
