#!/usr/bin/env python3
import csv
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path("/home/qcweb/rewrite-and-improve")
MANUAL = ROOT / "bitcoininfonews_action_review_404_manual_2026-06-09.csv"
INTERNAL = Path("/home/qcweb/bitcoininfonews/internal_html.csv")

STOPWORDS = {
    "the",
    "a",
    "an",
    "to",
    "of",
    "for",
    "in",
    "on",
    "and",
    "with",
    "after",
    "from",
    "as",
    "by",
    "at",
    "is",
    "its",
    "be",
    "set",
    "says",
    "amid",
    "into",
    "up",
    "new",
    "today",
    "what",
    "why",
    "how",
    "or",
    "via",
    "vs",
    "under",
    "over",
    "out",
    "off",
    "still",
    "now",
    "than",
    "near",
    "more",
    "less",
    "top",
}


def tokens(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t and t not in STOPWORDS]


def slug(url: str) -> str:
    return urlparse(url).path.strip("/").split("/")[-1]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    title_lookup = {}
    with INTERNAL.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            title_lookup[row["Address"]] = row.get("Title 1", "")

    promote_rows = []
    remain_rows = []

    with MANUAL.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            source_tokens = set(tokens(slug(row["url"])))
            title_tokens = set(tokens(title_lookup.get(row["suggested_target_url"], "")))
            title_cov = len(source_tokens & title_tokens) / max(1, len(source_tokens))
            score = float(row["score"])
            coverage = float(row["coverage"])
            seq = float(row["sequence_ratio"])

            promote = title_cov == 1.0 and score >= 0.72 and coverage >= 0.70
            payload = {
                **row,
                "title_token_coverage": f"{title_cov:.3f}",
            }
            if promote:
                promote_rows.append(payload)
            else:
                remain_rows.append(payload)

    action_301_rows = [
        {
            "source_url": row["url"],
            "target_url": row["suggested_target_url"],
            "source_title": "",
            "target_title": "",
            "reason": "Promoted from manual review: full title-token match with current winner.",
            "batch": "batch_1_internal_link_cleanup_and_404_mapping",
            "score": row["score"],
            "title_token_coverage": row["title_token_coverage"],
        }
        for row in promote_rows
    ]

    rankmath_rows = [
        {
            "id": "",
            "source": urlparse(row["url"]).path.lstrip("/") + (("?" + urlparse(row["url"]).query) if urlparse(row["url"]).query else ""),
            "matching": "exact",
            "destination": row["suggested_target_url"],
            "type": "301",
            "category": "",
            "status": "active",
            "ignore": "",
        }
        for row in promote_rows
    ]

    action_path = ROOT / "bitcoininfonews_action_301_now_from_manual_review_safe_2026-06-09.csv"
    rankmath_path = ROOT / "bitcoininfonews_rankmath_301_from_manual_review_safe_2026-06-09.csv"
    remain_path = ROOT / "bitcoininfonews_action_review_404_manual_residual_2026-06-09.csv"
    summary_path = ROOT / "bitcoininfonews_manual_404_review_promotion_summary_2026-06-09.md"

    write_csv(
        action_path,
        action_301_rows,
        ["source_url", "target_url", "source_title", "target_title", "reason", "batch", "score", "title_token_coverage"],
    )
    write_csv(
        rankmath_path,
        rankmath_rows,
        ["id", "source", "matching", "destination", "type", "category", "status", "ignore"],
    )
    write_csv(
        remain_path,
        remain_rows,
        ["url", "suggested_target_url", "score", "coverage", "sequence_ratio", "reason", "live_status_code", "live_location", "title_token_coverage"],
    )

    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write("# BitcoinInfoNews manual 404 review promotion summary\n\n")
        fh.write(f"- Promoted from manual review to safe 301: {len(promote_rows)}\n")
        fh.write(f"- Remaining true manual review rows: {len(remain_rows)}\n")
        fh.write("- Promotion rule: full title-token match with target live title, score >= 0.72, coverage >= 0.70.\n")

    print(action_path)
    print(rankmath_path)
    print(remain_path)
    print(summary_path)
    print("promoted", len(promote_rows))
    print("remaining", len(remain_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
