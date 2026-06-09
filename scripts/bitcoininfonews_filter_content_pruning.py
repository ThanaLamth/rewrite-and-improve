from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/home/qcweb/rewrite-and-improve")
CRAWL_ROOT = Path("/home/qcweb/bitcoininfonews")
INPUT_PATH = ROOT / "bitcoininfonews_action_review_content_pruning.csv"
INTERNAL_HTML_PATH = CRAWL_ROOT / "internal_html.csv"
PAGE_GSC_PATH = (
    CRAWL_ROOT
    / "GSC/bitcoininfonews.com-Performance-on-Search-2026-06-04/Trang.csv"
)

PRUNE_PATTERNS = {
    "brand_blockdag": ["blockdag", "blockdags", "bdag"],
    "brand_zkp": ["zero knowledge proof", "zkp", "zkps"],
    "brand_qubetics": ["qubetics"],
    "brand_cold_wallet": ["cold wallet", "coldwallet"],
    "brand_web3_ai": ["web3 ai", "web3ai"],
    "brand_unstaked": ["unstaked"],
    "brand_btfd": ["btfd"],
    "brand_arctic_pablo": ["arctic pablo"],
    "brand_dragoin": ["dragoin"],
    "brand_snorter": ["snorter"],
    "brand_moonbull": ["moonbull"],
    "brand_bullzilla": ["bullzilla"],
    "brand_bitcoin_hyper": ["bitcoin hyper"],
    "brand_pepenode": ["pepenode"],
    "brand_maxi_doge": ["maxi doge", "maxidoge"],
    "brand_pepeto": ["pepeto"],
    "brand_deepsnitch": ["deepsnitch"],
    "brand_spacepay": ["spacepay"],
    "brand_little_pepe": ["little pepe"],
    "brand_btc_bull": ["btc bull", "bitcoin bull"],
    "brand_best_wallet": ["best wallet"],
    "phrase_presale": ["presale", "presales", "presale auction"],
    "phrase_buy_now": ["buy now", "buy early", "best crypto to buy", "best presale"],
    "phrase_roi": ["roi", "100x", "500x", "1000x", "7000x", "10000x", "2900%"],
    "phrase_bonus": ["bonus", "2x offer", "2x bonus", "final100", "whitelist"],
    "phrase_hard_sell": ["limited time", "limited-time", "instant roi", "buyer battles"],
}

NOINDEX_PATTERNS = {
    "topic_price_prediction": ["price prediction", "price predictions", "forecast", "outlook"],
    "topic_meme_coin": ["meme coin", "meme coins"],
    "topic_generic_market": ["top crypto picks", "top crypto gems", "top meme coins", "coins to buy", "coins to watch"],
    "topic_analysis": ["technical analysis", "bullish", "rally", "surge", "surges", "gains", "climbs", "rises", "targets"],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_internal_html() -> dict[str, dict[str, str]]:
    data = {}
    for row in read_csv(INTERNAL_HTML_PATH):
        data[row["Address"].rstrip("/")] = row
    return data


def parse_float(value: str) -> float:
    if not value:
        return 0.0
    cleaned = value.replace("%", "").strip()
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")
    return float(cleaned)


def load_gsc_pages() -> dict[str, dict[str, float]]:
    data = {}
    for row in read_csv(PAGE_GSC_PATH):
        data[row["Trang hàng đầu"].rstrip("/")] = {
            "clicks": parse_float(row["Lượt nhấp"]),
            "impressions": parse_float(row["Lượt hiển thị"]),
            "position": parse_float(row["Vị trí"]) if row["Vị trí"] else 0.0,
        }
    return data


def find_matches(text: str, pattern_map: dict[str, list[str]]) -> list[str]:
    matches = []
    for label, patterns in pattern_map.items():
        if any(pattern in text for pattern in patterns):
            matches.append(label)
    return matches


def classify_row(
    row: dict[str, str],
    internal_html: dict[str, dict[str, str]],
    gsc_pages: dict[str, dict[str, float]],
) -> dict[str, object]:
    url = row["url"].rstrip("/")
    title = row["title"]
    text = f"{title} {url}".lower()
    crawl = internal_html.get(url, {})
    gsc = gsc_pages.get(url, {})

    prune_matches = find_matches(text, PRUNE_PATTERNS)
    noindex_matches = find_matches(text, NOINDEX_PATTERNS)

    clicks = gsc.get("clicks", 0.0)
    impressions = gsc.get("impressions", 0.0)
    position = gsc.get("position", 0.0)
    word_count = crawl.get("Word Count", "")
    inlinks = crawl.get("Inlinks", "")
    crawl_status = crawl.get("Status Code", "")
    indexability = crawl.get("Indexability", "")
    indexability_status = crawl.get("Indexability Status", "")

    if clicks >= 10:
        action = "keep_review"
        reason = "Has measurable GSC clicks; avoid pruning without manual editorial check."
        matched_rule = "traffic_exception"
    elif prune_matches:
        action = "prune_now"
        reason = "Strong promo/search-first brand or sales pattern."
        matched_rule = "|".join(prune_matches)
    elif noindex_matches:
        action = "keep_noindex_review"
        reason = "Search-first topical pattern, but softer than hard-sell promo pages."
        matched_rule = "|".join(noindex_matches)
    else:
        action = "keep_review"
        reason = "No strong prune pattern matched; keep for manual review."
        matched_rule = "fallback_review"

    return {
        "url": row["url"],
        "title": title,
        "action": action,
        "matched_rule": matched_rule,
        "reason": reason,
        "gsc_clicks": int(clicks) if clicks.is_integer() else clicks,
        "gsc_impressions": int(impressions) if impressions.is_integer() else impressions,
        "gsc_position": round(position, 2) if position else "",
        "crawl_status_code": crawl_status,
        "crawl_indexability": indexability,
        "crawl_indexability_status": indexability_status,
        "crawl_word_count": word_count,
        "crawl_inlinks": inlinks,
        "batch": row["batch"],
    }


def entity_bucket(text: str) -> str:
    ordered = [
        ("BlockDAG", ["blockdag", "blockdags", "bdag"]),
        ("Cold Wallet", ["cold wallet", "coldwallet"]),
        ("Qubetics", ["qubetics"]),
        ("Web3 ai", ["web3 ai", "web3ai"]),
        ("Unstaked", ["unstaked"]),
        ("BTFD", ["btfd"]),
        ("ZKP", ["zero knowledge proof", "zkp", "zkps"]),
        ("Arctic Pablo", ["arctic pablo"]),
        ("Dragoin", ["dragoin"]),
        ("Snorter", ["snorter"]),
        ("MoonBull", ["moonbull"]),
        ("Bullzilla", ["bullzilla"]),
        ("Bitcoin Hyper", ["bitcoin hyper"]),
        ("Meme Coin Generic", ["meme coin", "meme coins"]),
        ("Price Prediction Generic", ["price prediction", "price predictions", "forecast", "outlook"]),
    ]
    for label, patterns in ordered:
        if any(pattern in text for pattern in patterns):
            return label
    return "Other"


def main() -> None:
    internal_html = load_internal_html()
    gsc_pages = load_gsc_pages()
    input_rows = read_csv(INPUT_PATH)

    classified = [classify_row(row, internal_html, gsc_pages) for row in input_rows]

    prune_rows = [row for row in classified if row["action"] == "prune_now"]
    keep_noindex_rows = [row for row in classified if row["action"] == "keep_noindex_review"]
    keep_review_rows = [row for row in classified if row["action"] == "keep_review"]

    prune_rows.sort(key=lambda row: (entity_bucket(f"{row['title']} {row['url']}".lower()), row["url"]))
    keep_noindex_rows.sort(key=lambda row: row["url"])
    keep_review_rows.sort(key=lambda row: row["url"])

    fieldnames = list(classified[0].keys())

    prune_path = ROOT / "bitcoininfonews_action_prune_now_content_2026-06-09.csv"
    keep_noindex_path = ROOT / "bitcoininfonews_action_keep_noindex_content_2026-06-09.csv"
    keep_review_path = ROOT / "bitcoininfonews_action_keep_review_content_2026-06-09.csv"
    detail_path = ROOT / "bitcoininfonews_content_pruning_classified_2026-06-09.csv"
    summary_path = ROOT / "bitcoininfonews_content_pruning_summary_2026-06-09.md"

    write_csv(detail_path, classified, fieldnames)
    write_csv(prune_path, prune_rows, fieldnames)
    write_csv(keep_noindex_path, keep_noindex_rows, fieldnames)
    write_csv(keep_review_path, keep_review_rows, fieldnames)

    entity_counts = Counter()
    rule_counts = Counter()
    for row in prune_rows:
        text = f"{row['title']} {row['url']}".lower()
        entity_counts[entity_bucket(text)] += 1
        for part in str(row["matched_rule"]).split("|"):
            rule_counts[part] += 1

    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write("# BitcoinInfoNews content pruning summary\n\n")
        fh.write("## Output counts\n\n")
        fh.write(f"- Total reviewed: {len(classified)}\n")
        fh.write(f"- Prune now: {len(prune_rows)}\n")
        fh.write(f"- Keep but move to noindex review: {len(keep_noindex_rows)}\n")
        fh.write(f"- Keep for manual review: {len(keep_review_rows)}\n\n")

        fh.write("## Suggested batch order\n\n")
        for label, count in entity_counts.most_common():
            fh.write(f"- {label}: {count}\n")
        fh.write("\n")

        fh.write("## Strongest prune rules triggered\n\n")
        for label, count in rule_counts.most_common():
            fh.write(f"- {label}: {count}\n")
        fh.write("\n")

        if keep_review_rows:
            fh.write("## Keep review exceptions\n\n")
            for row in keep_review_rows:
                fh.write(
                    f"- {row['url']} | clicks={row['gsc_clicks']} | rule={row['matched_rule']}\n"
                )

    print(detail_path)
    print(prune_path)
    print(keep_noindex_path)
    print(keep_review_path)
    print(summary_path)


if __name__ == "__main__":
    main()
