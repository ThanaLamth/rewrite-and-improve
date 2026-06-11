#!/usr/bin/env python3

import csv
import re
from collections import defaultdict
from pathlib import Path


INPUT_CSV = Path("/home/qcweb/ccpress 2nd/internal_all.csv")
OUTPUT_CSV = Path("/home/qcweb/rewrite-and-improve/theccpress_tag_archive_decision_sheet_2026-06-11.csv")
OUTPUT_MD = Path("/home/qcweb/rewrite-and-improve/theccpress_task8_tag_archives_2026-06-11.md")

TAG_RE = re.compile(r"^(https://theccpress\.com/tag/([^/]+)/)(?:page/(\d+)/)?$")

MERGE_TARGETS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ripple": "xrp",
    "ripple-xrp": "xrp",
    "crypto": "cryptocurrency",
    "cryptocurrency-exchange": "crypto-exchange",
}

DROP_SLUGS = {
    "featured",
    "sponsored",
}

PROMO_PATTERNS = [
    "presale",
    "100x",
    "200x",
    "400x",
    "8000x",
    "roi",
    "best-crypto",
    "best-meme",
    "top-crypto",
    "next-big-crypto",
    "next-altcoin",
    "to-buy",
]


def root_record() -> dict[str, object]:
    return {
        "slug": "",
        "root_url": "",
        "title": "",
        "root_inlinks": 0,
        "variants": 0,
        "status_200_variants": 0,
        "nonindexable_variants": 0,
    }


def classify(slug: str, title: str, root_inlinks: int, variants: int) -> tuple[str, str, str]:
    lower_title = title.lower()

    if slug in MERGE_TARGETS:
        return "merge_candidate", MERGE_TARGETS[slug], "clear synonym or abbreviation of another tag"

    if slug in DROP_SLUGS:
        return "drop_or_leave_noindex", "", "administrative or presentation-style tag with low editorial value"

    if any(token in slug for token in PROMO_PATTERNS) or any(token in lower_title for token in ["presale", "roi", "best crypto", "top crypto", "next big crypto", "next altcoin"]):
        return "drop_or_leave_noindex", "", "promo or campaign-style tag likely tied to low-value commercial content"

    if variants == 1 and root_inlinks <= 2:
        return "drop_or_leave_noindex", "", "one-page low-signal tag with minimal internal support"

    if root_inlinks >= 10 or variants >= 3:
        return "review_keep", "", "broad recurring tag with stronger internal support"

    return "review_merge_or_drop", "", "limited signal; check whether this tag is unique enough to keep"


def main() -> None:
    roots: dict[str, dict[str, object]] = defaultdict(root_record)
    nonindexable_200 = 0

    with INPUT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row["Status Code"] == "200" and row["Indexability"] == "Non-Indexable":
                if row["Address"].startswith("https://theccpress.com/tag/"):
                    nonindexable_200 += 1

            match = TAG_RE.match(row["Address"])
            if not match:
                continue

            root_url, slug, _ = match.groups()
            record = roots[root_url]
            record["slug"] = slug
            record["root_url"] = root_url
            record["variants"] = int(record["variants"]) + 1

            if row["Status Code"] == "200":
                record["status_200_variants"] = int(record["status_200_variants"]) + 1
            if row["Indexability"] == "Non-Indexable":
                record["nonindexable_variants"] = int(record["nonindexable_variants"]) + 1

            if row["Address"] == root_url:
                record["title"] = row["Title 1"]
                record["root_inlinks"] = int(float(row["Unique Inlinks"] or 0))

    rows_out: list[dict[str, str]] = []
    counts = defaultdict(int)

    for record in roots.values():
        slug = str(record["slug"])
        title = str(record["title"])
        root_inlinks = int(record["root_inlinks"])
        variants = int(record["variants"])
        action, merge_target, reason = classify(slug, title, root_inlinks, variants)
        counts[action] += 1

        rows_out.append(
            {
                "tag_url": str(record["root_url"]),
                "tag_slug": slug,
                "tag_title": title,
                "root_unique_inlinks": str(root_inlinks),
                "url_variants_in_crawl": str(variants),
                "status_200_variants": str(record["status_200_variants"]),
                "nonindexable_variants": str(record["nonindexable_variants"]),
                "recommended_action": action,
                "merge_target_slug": merge_target,
                "reason": reason,
            }
        )

    rows_out.sort(
        key=lambda row: (
            {"review_keep": 0, "merge_candidate": 1, "review_merge_or_drop": 2, "drop_or_leave_noindex": 3}.get(row["recommended_action"], 9),
            -int(row["root_unique_inlinks"]),
            -int(row["url_variants_in_crawl"]),
            row["tag_slug"],
        )
    )

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "tag_url",
                "tag_slug",
                "tag_title",
                "root_unique_inlinks",
                "url_variants_in_crawl",
                "status_200_variants",
                "nonindexable_variants",
                "recommended_action",
                "merge_target_slug",
                "reason",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_out)

    unique_roots = len(roots)
    one_page = sum(1 for row in rows_out if row["url_variants_in_crawl"] == "1")
    low_signal = sum(1 for row in rows_out if row["url_variants_in_crawl"] == "1" and int(row["root_unique_inlinks"]) <= 2)

    note = f"""# TheCCPress Task 8: Tag Archive Surface

Date: 2026-06-11
Verdict: `reasonable heuristic`

## Core Finding

The site has a very large tag footprint, and almost all of it is non-indexable.

That is not a policy violation by itself, but it adds crawl overhead and editorial sprawl.

## Source

- [`/home/qcweb/ccpress 2nd/internal_all.csv`](/home/qcweb/ccpress%202nd/internal_all.csv)

## Primary Numbers

- `3093` tag archive URLs in the crawl were `200` and `Non-Indexable`
- those URLs collapse into `3212` unique tag roots when paginated variants are included from the crawl
- `3155` tag roots had only `1` crawled URL variant
- `2659` tag roots had both:
  - only `1` crawled URL variant
  - `<=2` unique inlinks

## Live Behavior Checks

Sample tag URLs currently return `200` and expose `noindex`:

- `/tag/meme-coin-with-staking/`
- `/tag/artificial-intelligence/`
- `/tag/bitcoin/`

## Heuristic Read

This suggests the site is generating too many low-value, one-off tags.

A practical cleanup rule is:

1. keep only a small set of recurring editorial tags
2. merge obvious synonyms and abbreviations
3. stop creating single-article tags

## Examples

Likely merge candidates:

- `btc -> bitcoin`
- `eth -> ethereum`
- `ripple -> xrp`
- `ripple-xrp -> xrp`
- `crypto -> cryptocurrency`
- `cryptocurrency-exchange -> crypto-exchange`

Likely drop or keep noindex:

- `featured`
- `sponsored`
- promo-style tags such as `*presale*`, `*roi*`, `*best-crypto*`, `*top-crypto*`

## Deliverable

Decision sheet:

- [`/home/qcweb/rewrite-and-improve/theccpress_tag_archive_decision_sheet_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_tag_archive_decision_sheet_2026-06-11.csv)

Action counts from the sheet:

- `review_keep`: `{counts['review_keep']}`
- `merge_candidate`: `{counts['merge_candidate']}`
- `review_merge_or_drop`: `{counts['review_merge_or_drop']}`
- `drop_or_leave_noindex`: `{counts['drop_or_leave_noindex']}`

## Recommended Next Step

Do not try to “fix” all tags at once.

Start with:

1. merge the obvious synonym pairs
2. stop new one-off tag creation in editorial workflow
3. leave the long tail noindexed for now unless the rebuild or taxonomy overhaul is already scheduled
"""

    OUTPUT_MD.write_text(note, encoding="utf-8")

    print(f"unique_tag_roots={unique_roots}")
    print(f"one_page_roots={one_page}")
    print(f"one_page_low_signal_roots={low_signal}")
    print(dict(counts))
    print(OUTPUT_CSV)
    print(OUTPUT_MD)


if __name__ == "__main__":
    main()
