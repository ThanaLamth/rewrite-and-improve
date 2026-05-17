#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import html
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
import xml.etree.ElementTree as ET


WP_NS = {"wp": "http://wordpress.org/export/1.2/"}
DC_NS = {"dc": "http://purl.org/dc/elements/1.1/"}
CONTENT_NS = {"content": "http://purl.org/rss/1.0/modules/content/"}
EXCERPT_NS = {"excerpt": "http://wordpress.org/export/1.2/excerpt/"}

SCRIPT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_ROOT.parent
DEFAULT_INPUT_ROOT = REPO_ROOT.parent
DEFAULT_OUTPUT_ROOT = REPO_ROOT
DEFAULT_INPUT_PATTERN = "coincu-latestcryptocurrencynewsandanalysis.WordPress.2026-05-05*.xml"

TOP_LEVEL_CATEGORIES = [
    "Knowledge",
    "Other Reviews",
    "Top Projects",
    "Exchange Reviews",
    "Crypto Millionaire",
    "DeFi Reviews",
    "CMC",
    "Casino Reviews",
    "Highlights",
    "GameFi Reviews",
    "Binance Square",
    "Analysis",
    "Ethereum",
    "Blockchain",
    "Airdrop",
    "DeFi",
    "Price Prediction",
    "Bitcoin",
    "Crypto Marketing",
]

SOURCE_LABELS = {
    0: "Main General Export",
    1: "Mixed Reviews Archive",
    2: "Casino / Gambling",
    3: "GameFi",
    4: "Protocol / DeFi Reviews",
    5: "Listicles / Roundups",
    6: "Price Predictions",
    7: "Exchange Reviews",
    8: "Net Worth / Celebrity",
}

STATUS_PRIORITY = {"publish": 0, "pending": 1, "draft": 2, "private": 3}

EXCHANGE_TITLE_PATTERNS = [
    r"\bexchanges?\b",
    r"\bcex\b",
    r"\bdex\b",
    r"\bswap\b",
    r"\bbroker\b",
]
WALLET_PATTERNS = [r"\bwallets?\b", r"account abstraction"]
CASINO_PATTERNS = [r"casino", r"sportsbook", r"gambl", r"\bbet\b", r"\bbetting\b", r"\bbookie\b"]
NET_WORTH_PATTERNS = [r"net worth"]
PRICE_PATTERNS = [r"price prediction", r"breakout", r"listing price"]
PROTOCOL_PATTERNS = [
    r"\bprotocol\b",
    r"\bnetwork\b",
    r"\bblockchain\b",
    r"\blayer 1\b",
    r"\blayer 2\b",
    r"\bl2\b",
    r"\brollup\b",
    r"\bzk\w*\b",
    r"\bstaking\b",
    r"\brestaking\b",
    r"\blending\b",
    r"\boracle\b",
    r"\bbridge\b",
    r"\bdefi\b",
    r"\bdepin\b",
    r"\becosystem\b",
    r"\bdata availability\b",
    r"\bliquidity\b",
    r"\byield\b",
    r"\blaunchpad\b",
    r"\binfrastructure\b",
]
COMPANY_PATTERNS = [
    r"\ba16z\b",
    r"\bventures\b",
    r"\bcapital\b",
    r"\bfund\b",
    r"\banalytics\b",
    r"\bpress releases?\b",
    r"\bbot\b",
    r"\bbots\b",
    r"\bincubator\b",
    r"\binvestment\b",
    r"\bbrands\b",
    r"\bcloud\b",
    r"\bscreener\b",
    r"\bmedia\b",
    r"\bevent\b",
]
LISTICLE_PATTERNS = [
    r"^\d+",
    r"\bbest\b",
    r"\btop \d+",
    r"\bguide\b",
    r"\boverview\b",
    r"\bhow to\b",
]
REVIEW_PATTERNS = [r"\breview\b", r"\breviews\b", r"^what is "]
COIN_HUB_EXCLUSION_PATTERNS = [
    r"\btrade\b",
    r"\btrading\b",
    r"\binvesting\b",
    r"\bico\b",
    r"\bido\b",
]


@dataclass
class RawPost:
    title: str
    slug: str
    url: str
    status: str
    post_date: str
    author: str
    primary_category: str
    categories: list[str]
    tags: list[str]
    word_count_estimate: int
    excerpt: str
    post_id: str
    source_export_cluster: str
    source_file: str


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def strip_html(value: str) -> str:
    if not value:
        return ""
    value = re.sub(r"<script\b[^>]*>.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b[^>]*>.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return normalize_space(html.unescape(value))


def text_or_empty(node: ET.Element | None) -> str:
    return normalize_space(node.text if node is not None and node.text else "")


def has_pattern(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def source_label_for_file(path: Path) -> str:
    match = re.search(r"\((\d+)\)\.xml$", path.name)
    suffix_number = int(match.group(1)) if match else 0
    return SOURCE_LABELS.get(suffix_number, f"Unknown Export {suffix_number}")


def source_sort_key(label: str) -> int:
    for number, candidate in SOURCE_LABELS.items():
        if candidate == label:
            return number
    return 999


def primary_category_for(categories: list[str]) -> str:
    for name in TOP_LEVEL_CATEGORIES:
        if name in categories:
            return name
    return categories[0] if categories else ""


def preferred_row_key(row: dict[str, str]) -> tuple[int, int, str]:
    return (
        STATUS_PRIORITY.get(row["status"], 99),
        -int(row["word_count_estimate"] or "0"),
        row["post_date"],
    )


def dedupe_key(row: dict[str, str]) -> str:
    for field in ("url", "slug", "title"):
        value = normalize_space(row[field]).lower()
        if value:
            return value
    return ""


def classify_cluster(row: dict[str, str]) -> str:
    title = row["title"].lower()
    primary_category = row["primary_category"]
    source_clusters = row["source_export_clusters"]
    text = " ".join(
        [
            title,
            row["categories"].lower(),
            row["tags"].lower(),
            primary_category.lower(),
            source_clusters.lower(),
        ]
    )

    if primary_category == "Crypto Millionaire" or has_pattern(text, NET_WORTH_PATTERNS):
        return "Net Worth / Celebrity"
    if primary_category == "Casino Reviews" or "Casino / Gambling" in source_clusters or has_pattern(text, CASINO_PATTERNS):
        return "Casino / Gambling"
    if primary_category == "Price Prediction" or "Price Predictions" in source_clusters or has_pattern(text, PRICE_PATTERNS):
        return "Price Predictions"
    if primary_category == "GameFi Reviews" or "GameFi" in source_clusters:
        return "GameFi"
    if primary_category == "Top Projects" or "Listicles / Roundups" in source_clusters:
        return "Listicles / Roundups"
    if primary_category == "Exchange Reviews" or "Exchange Reviews" in source_clusters:
        return "Exchange Reviews"
    if primary_category == "DeFi Reviews" or "Protocol / DeFi Reviews" in source_clusters:
        return "Protocol / Ecosystem Reviews"
    if has_pattern(text, WALLET_PATTERNS):
        return "Wallet Reviews"

    if primary_category in {
        "Knowledge",
        "Analysis",
        "Airdrop",
        "DeFi",
        "Ethereum",
        "Blockchain",
        "Bitcoin",
        "Crypto Marketing",
        "Highlights",
        "Binance Square",
    }:
        if has_pattern(title, LISTICLE_PATTERNS):
            return "Listicles / Roundups"
        return "General Crypto Content"

    if primary_category in {"Other Reviews", "CMC"} or has_pattern(title, REVIEW_PATTERNS):
        if has_pattern(title, EXCHANGE_TITLE_PATTERNS):
            return "Exchange Reviews"
        if has_pattern(text, COMPANY_PATTERNS):
            return "Company / Service Reviews"
        if has_pattern(text, PROTOCOL_PATTERNS):
            return "Protocol / Ecosystem Reviews"
        return "Coin / Project Reviews"

    if has_pattern(title, LISTICLE_PATTERNS):
        return "Listicles / Roundups"
    return "General Crypto Content"


def recommended_action_for(cluster: str) -> str:
    if cluster in {
        "Exchange Reviews",
        "Protocol / Ecosystem Reviews",
        "Coin / Project Reviews",
        "Wallet Reviews",
    }:
        return "keep"
    if cluster in {"Listicles / Roundups", "GameFi"}:
        return "merge_or_selective_keep"
    if cluster in {"Casino / Gambling", "Net Worth / Celebrity", "Price Predictions"}:
        return "deprioritize"
    if cluster == "Company / Service Reviews":
        return "selective_keep"
    return "selective_keep"


def hub_candidates_for(row: dict[str, str], cluster: str) -> list[str]:
    title = row["title"].lower()
    text = " ".join(
        [
            title,
            row["categories"].lower(),
            row["tags"].lower(),
            row["primary_category"].lower(),
            row["source_export_clusters"].lower(),
        ]
    )

    hubs: list[str] = []
    if cluster == "Exchange Reviews":
        explicit_exchange = (
            row["primary_category"] == "Exchange Reviews"
            or "Exchange Reviews" in row["source_export_clusters"]
            or has_pattern(title, EXCHANGE_TITLE_PATTERNS)
        )
        if explicit_exchange:
            hubs.append("Exchange Reviews")
    if cluster == "Protocol / Ecosystem Reviews":
        if (
            has_pattern(title, REVIEW_PATTERNS)
            or row["primary_category"] == "DeFi Reviews"
            or "Protocol / DeFi Reviews" in row["source_export_clusters"]
        ) and not has_pattern(text, COMPANY_PATTERNS):
            hubs.append("Protocol Reviews")
    if cluster == "Coin / Project Reviews":
        if (
            (has_pattern(title, REVIEW_PATTERNS) or row["primary_category"] == "CMC")
            and not has_pattern(text, COMPANY_PATTERNS)
            and not has_pattern(title, WALLET_PATTERNS)
            and not has_pattern(title, EXCHANGE_TITLE_PATTERNS)
            and not has_pattern(title, COIN_HUB_EXCLUSION_PATTERNS)
        ):
            hubs.append("Coin Reviews")
    return hubs


def why_fit_for_hub(row: dict[str, str], hub_name: str) -> str:
    if hub_name == "Exchange Reviews":
        if row["primary_category"] == "Exchange Reviews":
            return "explicit exchange category"
        if "Exchange Reviews" in row["source_export_clusters"]:
            return "exchange export bucket"
        return "exchange-specific title intent"
    if hub_name == "Protocol Reviews":
        if row["primary_category"] == "DeFi Reviews":
            return "explicit DeFi/protocol category"
        if "Protocol / DeFi Reviews" in row["source_export_clusters"]:
            return "protocol export bucket"
        return "protocol/ecosystem review intent"
    return "coin/project review intent"


def parse_post_item(item: ET.Element, source_path: Path) -> RawPost | None:
    post_type = text_or_empty(item.find("wp:post_type", WP_NS))
    if post_type != "post":
        return None

    title = text_or_empty(item.find("title"))
    url = text_or_empty(item.find("link"))
    slug = text_or_empty(item.find("wp:post_name", WP_NS))
    status = text_or_empty(item.find("wp:status", WP_NS))
    post_date = text_or_empty(item.find("wp:post_date", WP_NS))
    author = text_or_empty(item.find("dc:creator", DC_NS))
    post_id = text_or_empty(item.find("wp:post_id", WP_NS))

    categories: list[str] = []
    tags: list[str] = []
    for category_node in item.findall("category"):
        domain = category_node.attrib.get("domain", "")
        name = normalize_space(category_node.text or "")
        if not name:
            continue
        if domain == "category":
            categories.append(name)
        elif domain == "post_tag":
            tags.append(name)

    content_html = text_or_empty(item.find("content:encoded", CONTENT_NS))
    excerpt_text = text_or_empty(item.find("excerpt:encoded", EXCERPT_NS))
    content_text = strip_html(content_html)
    excerpt = excerpt_text or content_text[:280]
    word_count_estimate = len(re.findall(r"\b\w+\b", content_text))

    return RawPost(
        title=title,
        slug=slug,
        url=url,
        status=status,
        post_date=post_date,
        author=author,
        primary_category=primary_category_for(categories),
        categories=categories,
        tags=tags,
        word_count_estimate=word_count_estimate,
        excerpt=excerpt,
        post_id=post_id,
        source_export_cluster=source_label_for_file(source_path),
        source_file=source_path.name,
    )


def parse_export(path: Path) -> list[dict[str, str]]:
    root = ET.parse(path).getroot()
    channel = root.find("channel")
    if channel is None:
        return []

    rows: list[dict[str, str]] = []
    for item in channel.findall("item"):
        parsed = parse_post_item(item, path)
        if parsed is None:
            continue
        rows.append(
            {
                "title": parsed.title,
                "slug": parsed.slug,
                "url": parsed.url,
                "status": parsed.status,
                "post_date": parsed.post_date,
                "author": parsed.author,
                "primary_category": parsed.primary_category,
                "categories": " | ".join(parsed.categories),
                "tags": " | ".join(parsed.tags),
                "word_count_estimate": str(parsed.word_count_estimate),
                "cluster": "",
                "recommended_action": "",
                "hub_candidates": "",
                "source_export_clusters": parsed.source_export_cluster,
                "source_files": parsed.source_file,
                "post_ids": parsed.post_id,
                "occurrences": "1",
                "excerpt": parsed.excerpt,
            }
        )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_unique_rows(raw_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in raw_rows:
        grouped[dedupe_key(row)].append(row)

    unique_rows: list[dict[str, str]] = []
    for rows in grouped.values():
        best = min(rows, key=preferred_row_key)
        merged = dict(best)
        merged["source_export_clusters"] = " | ".join(
            sorted({row["source_export_clusters"] for row in rows}, key=source_sort_key)
        )
        merged["source_files"] = " | ".join(sorted({row["source_files"] for row in rows}))
        merged["post_ids"] = " | ".join(sorted({row["post_ids"] for row in rows if row["post_ids"]}))
        merged["occurrences"] = str(len(rows))

        cluster = classify_cluster(merged)
        hubs = hub_candidates_for(merged, cluster)
        merged["cluster"] = cluster
        merged["recommended_action"] = recommended_action_for(cluster)
        merged["hub_candidates"] = " | ".join(hubs)
        unique_rows.append(merged)

    unique_rows.sort(key=lambda row: (row["cluster"], row["title"].lower()))
    return unique_rows


def build_hub_rows(unique_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    hub_rows: list[dict[str, str]] = []
    for row in unique_rows:
        hubs = [hub.strip() for hub in row["hub_candidates"].split("|") if hub.strip()]
        for hub_name in hubs:
            hub_rows.append(
                {
                    "hub_name": hub_name,
                    "title": row["title"],
                    "url": row["url"],
                    "status": row["status"],
                    "post_date": row["post_date"],
                    "primary_category": row["primary_category"],
                    "cluster": row["cluster"],
                    "recommended_action": row["recommended_action"],
                    "source_export_clusters": row["source_export_clusters"],
                    "occurrences": row["occurrences"],
                    "why_fit": why_fit_for_hub(row, hub_name),
                }
            )
    hub_rows.sort(key=lambda row: (row["hub_name"], STATUS_PRIORITY.get(row["status"], 99), row["title"].lower()))
    return hub_rows


def build_markdown_summary(
    raw_rows: list[dict[str, str]],
    unique_rows: list[dict[str, str]],
    hub_rows: list[dict[str, str]],
    output_root: Path,
) -> str:
    raw_source_counts = Counter(row["source_export_clusters"] for row in raw_rows)
    duplicate_count = sum(1 for row in unique_rows if int(row["occurrences"]) > 1)
    status_counts = Counter(row["status"] for row in unique_rows)
    cluster_counts = Counter(row["cluster"] for row in unique_rows)
    hub_counts = Counter(row["hub_name"] for row in hub_rows)

    cluster_examples: dict[str, list[str]] = defaultdict(list)
    cluster_status: dict[str, Counter[str]] = defaultdict(Counter)
    for row in unique_rows:
        cluster_status[row["cluster"]][row["status"]] += 1
        if row["status"] == "publish" and len(cluster_examples[row["cluster"]]) < 6:
            cluster_examples[row["cluster"]].append(row["title"])

    cluster_actions = {
        "Exchange Reviews": "keep",
        "Protocol / Ecosystem Reviews": "keep",
        "Coin / Project Reviews": "keep",
        "Wallet Reviews": "keep",
        "Company / Service Reviews": "selective_keep",
        "Listicles / Roundups": "merge_or_selective_keep",
        "GameFi": "merge_or_selective_keep",
        "General Crypto Content": "selective_keep",
        "Price Predictions": "deprioritize",
        "Casino / Gambling": "deprioritize",
        "Net Worth / Celebrity": "deprioritize",
    }
    cluster_order = [
        "Exchange Reviews",
        "Protocol / Ecosystem Reviews",
        "Coin / Project Reviews",
        "Wallet Reviews",
        "Company / Service Reviews",
        "Listicles / Roundups",
        "GameFi",
        "General Crypto Content",
        "Price Predictions",
        "Casino / Gambling",
        "Net Worth / Celebrity",
    ]

    output_root = output_root.resolve()

    lines: list[str] = []
    lines.append("# Coincu Export Analysis")
    lines.append("")
    lines.append(f"Last updated: {date.today().isoformat()}")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"- Parsed source files: `{len(raw_source_counts)}`")
    lines.append(f"- Raw post records across all files: `{len(raw_rows)}`")
    lines.append(f"- Unique posts after dedupe by URL/slug/title: `{len(unique_rows)}`")
    lines.append(f"- Raw inventory CSV: `{output_root / 'coincu_export_posts_inventory_raw.csv'}`")
    lines.append(f"- Unique inventory CSV: `{output_root / 'coincu_export_posts_inventory.csv'}`")
    lines.append(f"- Hub candidates CSV: `{output_root / 'coincu_hub_candidates.csv'}`")
    lines.append("")
    lines.append("## Source Files")
    lines.append("")
    for label in sorted(raw_source_counts, key=source_sort_key):
        lines.append(f"- `{label}`: `{raw_source_counts[label]}` post records")
    lines.append("")
    lines.append("## Duplicate Summary")
    lines.append("")
    lines.append(f"- Unique-only posts: `{sum(1 for row in unique_rows if int(row['occurrences']) == 1)}`")
    lines.append(f"- Posts appearing in more than one export: `{duplicate_count}`")
    lines.append("")
    lines.append("## Status Summary")
    lines.append("")
    for status, count in status_counts.most_common():
        lines.append(f"- `{status}`: `{count}`")
    lines.append("")
    lines.append("## Cluster Recommendations")
    lines.append("")
    for cluster in cluster_order:
        if cluster not in cluster_counts:
            continue
        lines.append(f"### {cluster}")
        lines.append("")
        lines.append(f"- Count: `{cluster_counts[cluster]}`")
        lines.append(f"- Recommended action: `{cluster_actions[cluster]}`")
        status_mix = ", ".join(f"{status}={count}" for status, count in cluster_status[cluster].most_common())
        lines.append(f"- Status mix: `{status_mix}`")
        lines.append("- Example published posts:")
        for title in cluster_examples[cluster]:
            lines.append(f"  - `{title}`")
        lines.append("")

    lines.append("## Strongest Topical Assets")
    lines.append("")
    lines.append("- `Exchange Reviews` is the cleanest commercial-intent review bucket and fits a dedicated hub immediately.")
    lines.append("- `Protocol / Ecosystem Reviews` is the best long-term authority bucket for scalable crypto topical depth.")
    lines.append("- `Coin / Project Reviews` is usable for a focused review hub once weaker service/company pages are excluded from hub templates.")
    lines.append("")
    lines.append("## Weakest Topical Assets")
    lines.append("")
    lines.append("- `Net Worth / Celebrity` is the clearest off-topic bucket for a crypto research brand.")
    lines.append("- `Casino / Gambling` is its own vertical and weakens a cleaner crypto-expertise positioning.")
    lines.append("- `Price Predictions` is the weakest trust-aligned bucket if the goal is stronger expertise signals.")
    lines.append("")
    lines.append("## Hub Candidate Counts")
    lines.append("")
    for hub_name in ("Coin Reviews", "Protocol Reviews", "Exchange Reviews"):
        lines.append(f"- `{hub_name}`: `{hub_counts.get(hub_name, 0)}` mapped posts")
    lines.append("")
    lines.append("## Practical next steps")
    lines.append("")
    lines.append("- Use the unique inventory CSV to filter by `cluster`, `status`, `recommended_action`, and `source_export_clusters`.")
    lines.append("- Use the hub candidates CSV to shortlist `Coin Reviews`, `Protocol Reviews`, and `Exchange Reviews` pages.")
    lines.append("- Use the raw inventory CSV if you need to inspect duplicates or trace which export each page came from.")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze Coincu WordPress exports and build hub planning files.")
    parser.add_argument(
        "--input-root",
        type=Path,
        default=DEFAULT_INPUT_ROOT,
        help="Directory that contains the WordPress XML exports.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory where CSV and markdown outputs should be written.",
    )
    parser.add_argument(
        "--input-pattern",
        default=DEFAULT_INPUT_PATTERN,
        help="Glob pattern used to locate WordPress XML exports inside the input root.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_root = args.input_root.expanduser().resolve()
    output_root = args.output_root.expanduser().resolve()

    source_paths = sorted(
        input_root.glob(args.input_pattern),
        key=lambda path: int(re.search(r"\((\d+)\)\.xml$", path.name).group(1)) if re.search(r"\((\d+)\)\.xml$", path.name) else 0,
    )
    if not source_paths:
        raise SystemExit(
            f"No Coincu XML exports found under {input_root} matching {args.input_pattern}."
        )

    raw_rows: list[dict[str, str]] = []
    for path in source_paths:
        raw_rows.extend(parse_export(path))

    unique_rows = build_unique_rows(raw_rows)
    hub_rows = build_hub_rows(unique_rows)

    raw_fieldnames = [
        "title",
        "slug",
        "url",
        "status",
        "post_date",
        "author",
        "primary_category",
        "categories",
        "tags",
        "word_count_estimate",
        "cluster",
        "recommended_action",
        "hub_candidates",
        "source_export_clusters",
        "source_files",
        "post_ids",
        "occurrences",
        "excerpt",
    ]
    hub_fieldnames = [
        "hub_name",
        "title",
        "url",
        "status",
        "post_date",
        "primary_category",
        "cluster",
        "recommended_action",
        "source_export_clusters",
        "occurrences",
        "why_fit",
    ]

    output_root.mkdir(parents=True, exist_ok=True)

    write_csv(output_root / "coincu_export_posts_inventory_raw.csv", raw_fieldnames, raw_rows)
    write_csv(output_root / "coincu_export_posts_inventory.csv", raw_fieldnames, unique_rows)
    write_csv(output_root / "coincu_hub_candidates.csv", hub_fieldnames, hub_rows)
    (output_root / "coincu_content_cluster_recommendations.md").write_text(
        build_markdown_summary(raw_rows, unique_rows, hub_rows, output_root),
        encoding="utf-8",
    )

    print(f"Parsed raw post records: {len(raw_rows)}")
    print(f"Unique posts after dedupe: {len(unique_rows)}")
    print(f"Hub candidates written: {len(hub_rows)}")


if __name__ == "__main__":
    main()
