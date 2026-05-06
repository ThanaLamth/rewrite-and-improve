#!/usr/bin/env python3
"""Watch Google Trends RSS and send crypto/markets/policy items to Telegram."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import escape, unescape
from pathlib import Path
from typing import Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


USER_AGENT = "google-trends-finance-watch/1.0 (+https://trends.google.com/)"
RSS_NS = {"ht": "https://trends.google.com/trending/rss", "atom": "http://www.w3.org/2005/Atom"}
DEFAULT_FEED = "https://trends.google.com/trending/rss?geo=US"
DEFAULT_MAX_MESSAGE_LEN = 3800
DEFAULT_GEOS = ["US"]

GEO_NAME_BY_CODE = {
    "AE": "UAE",
    "SG": "Singapore",
    "TR": "Türkiye",
    "AR": "Argentina",
    "TH": "Thailand",
    "BR": "Brazil",
    "VN": "Vietnam",
    "US": "United States",
    "SA": "Saudi Arabia",
    "MY": "Malaysia",
    "HK": "Hong Kong",
    "ID": "Indonesia",
    "KR": "South Korea",
    "ZA": "South Africa",
    "CH": "Switzerland",
    "PH": "Philippines",
    "VE": "Venezuela",
    "UA": "Ukraine",
    "CA": "Canada",
    "SI": "Slovenia",
    "MX": "Mexico",
    "AU": "Australia",
    "LU": "Luxembourg",
    "CL": "Chile",
    "IE": "Ireland",
    "NO": "Norway",
    "BE": "Belgium",
    "CY": "Cyprus",
    "DE": "Germany",
    "IN": "India",
}

GEO_ALIASES = {
    "uae": "AE",
    "united arab emirates": "AE",
    "singapore": "SG",
    "turkiye": "TR",
    "türkiye": "TR",
    "turkey": "TR",
    "argentina": "AR",
    "thailand": "TH",
    "brazil": "BR",
    "vietnam": "VN",
    "united states": "US",
    "usa": "US",
    "us": "US",
    "saudi arabia": "SA",
    "malaysia": "MY",
    "hong kong": "HK",
    "indonesia": "ID",
    "south korea": "KR",
    "korea": "KR",
    "south africa": "ZA",
    "switzerland": "CH",
    "philippines": "PH",
    "venezuela": "VE",
    "ukraine": "UA",
    "canada": "CA",
    "slovenia": "SI",
    "mexico": "MX",
    "australia": "AU",
    "luxembourg": "LU",
    "chile": "CL",
    "ireland": "IE",
    "norway": "NO",
    "belgium": "BE",
    "cyprus": "CY",
    "germany": "DE",
    "india": "IN",
}

CRYPTO_TERMS = {
    "bitcoin",
    "btc",
    "ethereum",
    "eth",
    "crypto",
    "cryptocurrency",
    "digital asset",
    "digital assets",
    "token",
    "tokens",
    "coin",
    "coins",
    "altcoin",
    "altcoins",
    "stablecoin",
    "stablecoins",
    "memecoin",
    "memecoins",
    "blockchain",
    "blockchains",
    "web3",
    "wallet",
    "wallets",
    "exchange",
    "exchanges",
    "defi",
    "mining",
    "miner",
    "miners",
}

WEAK_CRYPTO_TERMS = {
    "coin",
    "coins",
    "token",
    "tokens",
    "wallet",
    "wallets",
    "exchange",
    "exchanges",
    "mining",
    "miner",
    "miners",
}

FINANCE_TERMS = {
    "etf",
    "etfs",
    "stocks",
    "stock",
    "shares",
    "earnings",
    "nasdaq",
    "dow",
    "s&p",
    "sp500",
    "fed",
    "fomc",
    "inflation",
    "cpi",
    "ppi",
    "mortgage",
    "treasury",
    "treasuries",
    "bond",
    "bonds",
    "bank",
    "banks",
    "ipo",
    "recession",
    "tariff",
    "tariffs",
    "oil",
    "gold",
    "silver",
    "forex",
    "dollar",
    "usd",
    "vix",
    "pmi",
    "market cap",
    "yield",
    "yields",
}

BUSINESS_TERMS = {
    "deal",
    "merger",
    "acquisition",
    "acquires",
    "acquire",
    "acquired",
    "revenue",
    "profit",
    "loss",
    "losses",
    "funding",
    "valuation",
    "settlement",
    "lawsuit",
    "price target",
    "guidance",
    "ceo",
    "cfo",
    "quarter",
    "quarterly",
    "results",
    "forecast",
    "sales",
    "dividend",
}

POLICY_TERMS = {
    "sec",
    "congress",
    "senate",
    "house",
    "white house",
    "trump",
    "tariff",
    "tariffs",
    "fed",
    "fomc",
    "treasury",
    "law",
    "bill",
    "regulation",
    "regulatory",
    "policy",
    "policies",
    "sanctions",
    "election",
    "executive order",
    "doj",
    "department of justice",
}

MARKETS_SOURCES = {
    "bloomberg",
    "cnbc",
    "marketwatch",
    "yahoo finance",
    "reuters",
    "financial times",
    "the wall street journal",
    "wsj",
    "forbes",
    "investopedia",
    "investor's business daily",
    "coindesk",
    "cointelegraph",
    "the block",
    "decrypt",
    "benzinga",
    "seeking alpha",
    "barron's",
    "fortune",
    "business insider",
    "wsj",
}

CRYPTO_SOURCES = {
    "coindesk",
    "cointelegraph",
    "the block",
    "decrypt",
    "bitcoin magazine",
    "blockworks",
    "crypto.news",
}

CRYPTO_ENTITIES = {
    "binance",
    "coinbase",
    "ripple",
    "xrp",
    "solana",
    "bnb",
    "dogecoin",
    "toncoin",
    "ton",
    "tron",
    "cardano",
    "ada",
    "usdt",
    "usdc",
    "tether",
    "circle",
}

PUBLIC_COMPANIES = {
    "apple",
    "tesla",
    "nvidia",
    "microsoft",
    "google",
    "alphabet",
    "meta",
    "amazon",
    "netflix",
    "intel",
    "amd",
    "openai",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watch Google Trends RSS and send crypto/markets/policy items to Telegram."
    )
    parser.add_argument(
        "--feed",
        default=os.environ.get("GOOGLE_TRENDS_RSS_URL", DEFAULT_FEED),
        help="Google Trends RSS URL. Defaults to US Trending now feed.",
    )
    parser.add_argument(
        "--geo",
        action="append",
        default=[],
        help="Google Trends geo code or country name. Repeat or pass comma-separated values.",
    )
    parser.add_argument(
        "--state",
        default=os.path.expanduser("~/.codex/memories/google-trends-finance-state.json"),
        help="Path to persisted state JSON file.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--send-telegram",
        action="store_true",
        help="Send Telegram alerts for new crypto/markets/policy trend items.",
    )
    parser.add_argument(
        "--telegram-token",
        default=os.environ.get("TELEGRAM_BOT_TOKEN"),
        help="Telegram bot token. Defaults to TELEGRAM_BOT_TOKEN.",
    )
    parser.add_argument(
        "--telegram-chat-id",
        default=os.environ.get("TELEGRAM_CHAT_ID"),
        help="Telegram chat id. Defaults to TELEGRAM_CHAT_ID.",
    )
    parser.add_argument(
        "--telegram-thread-id",
        default=os.environ.get("TELEGRAM_TRENDS_THREAD_ID") or os.environ.get("TELEGRAM_MESSAGE_THREAD_ID"),
        help="Telegram topic thread id. Defaults to TELEGRAM_TRENDS_THREAD_ID or TELEGRAM_MESSAGE_THREAD_ID.",
    )
    parser.add_argument(
        "--send-empty-test",
        action="store_true",
        help="Send a test/baseline summary even when there are no new matched items.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print matched items without sending Telegram or saving state.",
    )
    return parser.parse_args()


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value or "")).strip()


def contains_term(blob: str, term: str) -> bool:
    if re.fullmatch(r"[a-z0-9]+", term):
        return re.search(rf"\b{re.escape(term)}\b", blob) is not None
    return term in blob


def count_hits(blob: str, terms: set[str]) -> int:
    return sum(1 for term in terms if contains_term(blob, term))


def fetch_feed_xml(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def resolve_geos(raw_values: List[str], env_value: str | None, fallback_feed: str) -> List[str]:
    values: List[str] = []
    for raw in raw_values:
        values.extend(part.strip() for part in raw.split(",") if part.strip())
    if env_value:
        values.extend(part.strip() for part in env_value.split(",") if part.strip())
    if not values:
        match = re.search(r"[?&]geo=([A-Za-z]{2})\b", fallback_feed)
        if match:
            values.append(match.group(1))
    if not values:
        values.extend(DEFAULT_GEOS)

    resolved: List[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized:
            continue
        upper = normalized.upper()
        if re.fullmatch(r"[A-Z]{2}", upper):
            code = upper
        else:
            alias_key = normalized.casefold()
            code = GEO_ALIASES.get(alias_key)
            if not code:
                raise ValueError(f"Unsupported geo value: {value}")
        if code not in resolved:
            resolved.append(code)
    return resolved


def geo_feed_url(geo_code: str) -> str:
    return f"https://trends.google.com/trending/rss?geo={geo_code}"


def parse_feed(xml_text: str, geo_code: str) -> List[Dict[str, object]]:
    root = ET.fromstring(xml_text)
    items: List[Dict[str, object]] = []
    for item in root.findall("./channel/item"):
        title = normalize_space(item.findtext("title"))
        approx_traffic = normalize_space(item.findtext("ht:approx_traffic", namespaces=RSS_NS))
        pub_date = normalize_space(item.findtext("pubDate"))
        news_items = []
        for news in item.findall("ht:news_item", RSS_NS):
            news_items.append(
                {
                    "title": normalize_space(news.findtext("ht:news_item_title", namespaces=RSS_NS)),
                    "url": normalize_space(news.findtext("ht:news_item_url", namespaces=RSS_NS)),
                    "source": normalize_space(news.findtext("ht:news_item_source", namespaces=RSS_NS)),
                }
            )
        item_id = f"{geo_code}|{title}|{pub_date}"
        items.append(
            {
                "id": item_id,
                "geo_code": geo_code,
                "geo_name": GEO_NAME_BY_CODE.get(geo_code, geo_code),
                "title": title,
                "approx_traffic": approx_traffic,
                "pub_date": pub_date,
                "news_items": news_items,
            }
        )
    return items


def finance_score(item: Dict[str, object]) -> int:
    title = str(item.get("title", ""))
    news_items = item.get("news_items", []) or []
    blob_parts = [title.lower()]
    source_names = []
    for news in news_items:
        news_title = str(news.get("title", ""))
        news_source = str(news.get("source", ""))
        news_url = str(news.get("url", ""))
        blob_parts.extend([news_title.lower(), news_source.lower(), news_url.lower()])
        if news_source:
            source_names.append(news_source.lower())
    blob = " ".join(blob_parts)

    score = 0
    for term in CRYPTO_TERMS - WEAK_CRYPTO_TERMS:
        if contains_term(blob, term):
            score += 4
    for term in WEAK_CRYPTO_TERMS:
        if contains_term(blob, term):
            score += 1
    for term in FINANCE_TERMS:
        if contains_term(blob, term):
            score += 3
    for term in BUSINESS_TERMS:
        if contains_term(blob, term):
            score += 1
    for term in POLICY_TERMS:
        if contains_term(blob, term):
            score += 1
    for source in MARKETS_SOURCES | CRYPTO_SOURCES:
        if any(source in candidate for candidate in source_names):
            score += 2
    if re.search(r"\$\d", blob):
        score += 1
    if any(contains_term(blob, company) for company in PUBLIC_COMPANIES):
        score += 1
    return score


def is_finance_related(item: Dict[str, object]) -> bool:
    score = finance_score(item)
    title_blob = str(item.get("title", "")).lower()
    news_blob = " ".join(
        f"{news.get('title', '')} {news.get('source', '')}".lower()
        for news in (item.get("news_items", []) or [])
    )
    all_blob = f"{title_blob} {news_blob}".strip()

    title_strong_crypto_hits = count_hits(title_blob, CRYPTO_TERMS - WEAK_CRYPTO_TERMS)
    title_weak_crypto_hits = count_hits(title_blob, WEAK_CRYPTO_TERMS)
    title_crypto_entity_hits = count_hits(title_blob, CRYPTO_ENTITIES)
    title_finance_hits = count_hits(title_blob, FINANCE_TERMS)
    title_business_hits = count_hits(title_blob, BUSINESS_TERMS)
    title_policy_hits = count_hits(title_blob, POLICY_TERMS)
    title_company_hits = count_hits(title_blob, PUBLIC_COMPANIES)

    news_strong_crypto_hits = count_hits(news_blob, CRYPTO_TERMS - WEAK_CRYPTO_TERMS)
    news_weak_crypto_hits = count_hits(news_blob, WEAK_CRYPTO_TERMS)
    news_crypto_entity_hits = count_hits(news_blob, CRYPTO_ENTITIES)
    news_finance_hits = count_hits(news_blob, FINANCE_TERMS)
    news_business_hits = count_hits(news_blob, BUSINESS_TERMS)
    news_policy_hits = count_hits(news_blob, POLICY_TERMS)
    news_company_hits = count_hits(news_blob, PUBLIC_COMPANIES)
    market_source_hits = sum(1 for source in MARKETS_SOURCES if source in news_blob)
    crypto_source_hits = sum(1 for source in CRYPTO_SOURCES if source in news_blob)

    strong_crypto_hits = title_strong_crypto_hits + news_strong_crypto_hits
    crypto_hits = strong_crypto_hits + title_weak_crypto_hits + news_weak_crypto_hits

    if title_strong_crypto_hits > 0 or title_crypto_entity_hits > 0:
        return True
    if title_weak_crypto_hits > 0 and (news_finance_hits > 0 or crypto_source_hits > 0 or market_source_hits > 0):
        return True
    if title_finance_hits > 0 and (
        market_source_hits > 0
        or news_business_hits > 0
        or news_policy_hits > 0
        or title_company_hits > 0
        or news_company_hits > 0
    ):
        return True
    if title_business_hits > 0 and title_company_hits > 0 and (
        market_source_hits > 0 or news_finance_hits > 0 or news_policy_hits > 0
    ):
        return True
    if title_policy_hits > 0 and (
        news_finance_hits > 0
        or news_strong_crypto_hits > 0
        or news_crypto_entity_hits > 0
        or market_source_hits > 0
        or crypto_source_hits > 0
    ):
        return True
    if title_company_hits > 0 and (
        title_finance_hits > 0 or news_finance_hits > 0 or news_business_hits > 0 or market_source_hits > 0
    ):
        return True
    return score >= 8 and (
        title_finance_hits > 0
        or title_policy_hits > 0
        or title_company_hits > 0
        or title_strong_crypto_hits > 0
        or title_crypto_entity_hits > 0
        or (title_weak_crypto_hits > 0 and (news_finance_hits > 0 or crypto_source_hits > 0 or market_source_hits > 0))
        or (title_business_hits > 0 and title_company_hits > 0)
        or ("crypto" in all_blob and market_source_hits > 0)
        or (crypto_hits > 0 and news_finance_hits > 0)
    )


def load_state(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"seen_ids": []}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return {"seen_ids": data.get("seen_ids", [])}


def save_state(path: Path, seen_ids: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "seen_ids": seen_ids[:200],
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=True, indent=2, sort_keys=True)


def merge_seen_ids(previous: List[str], current: List[str]) -> List[str]:
    merged: List[str] = []
    for item_id in current + previous:
        if item_id and item_id not in merged:
            merged.append(item_id)
    return merged[:200]


def build_report(
    items: List[Dict[str, object]],
    matched: List[Dict[str, object]],
    new_items: List[Dict[str, object]],
    errors: List[str],
) -> str:
    lines = [
        f"Feed items: {len(items)}",
        f"Filtered matches: {len(matched)}",
        f"New filtered matches: {len(new_items)}",
    ]
    if errors:
        lines.append(f"Geo errors: {len(errors)}")
        lines.extend(f"! {error}" for error in errors)
    for item in new_items or matched[:10]:
        lines.append(
            f"- [{item['geo_code']}] {item['title']} | {item['approx_traffic']} | {item['pub_date']}"
        )
    return "\n".join(lines)


def format_trend_block(item: Dict[str, object], index: int, max_news: int = 3) -> str:
    geo_code = escape(str(item.get("geo_code", "")))
    geo_name = escape(str(item.get("geo_name", geo_code)))
    title = escape(str(item["title"]))
    traffic = escape(str(item["approx_traffic"]))
    lines = [f"{index}. [{geo_code}] {geo_name}: {title} ({traffic})"]
    for news in (item.get("news_items", []) or [])[:max_news]:
        source = escape(str(news.get("source", "")).strip() or "Source")
        url = str(news.get("url", "")).strip()
        if url:
            lines.append(f'{source}: <a href="{escape(url, quote=True)}">link</a>')
    return "\n".join(lines)


def build_messages(
    items: List[Dict[str, object]],
    geos: List[str],
    send_empty_test: bool,
    first_run: bool,
    errors: List[str],
) -> List[str]:
    if not items and not send_empty_test:
        return []
    prefix = "Google Trends crypto / markets / policy"
    geo_summary = ", ".join(geos)
    if first_run and send_empty_test:
        header = f"{prefix}\n\nGEOs: {geo_summary}\nBaseline created."
    elif send_empty_test and not items:
        header = f"{prefix}\n\nGEOs: {geo_summary}\nTest run: no filtered matches right now."
    else:
        header = f"{prefix}\n\nGEOs: {geo_summary}"
    if errors:
        header = f"{header}\nGeo errors: {'; '.join(errors)}"

    blocks = [format_trend_block(item, index) for index, item in enumerate(items, 1)]

    messages: List[str] = []
    current = header
    for block in blocks:
        candidate = f"{current}\n\n{block}"
        if len(candidate) <= DEFAULT_MAX_MESSAGE_LEN:
            current = f"{current}\n\n{block}"
        else:
            messages.append(current)
            current = f"{prefix} (continued)\n\n{block}"
    if current.strip():
        messages.append(current)
    if not blocks and send_empty_test:
        messages = [header]
    return messages


def send_telegram(token: str, chat_id: str, message: str, timeout: int, thread_id: str | None) -> None:
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if thread_id:
        payload["message_thread_id"] = int(thread_id)
    data = json.dumps(payload).encode("utf-8")
    request = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        response.read()


def main() -> int:
    args = parse_args()
    state_path = Path(os.path.expanduser(args.state))
    state = load_state(state_path)
    previous_seen_ids = state.get("seen_ids", [])
    first_run = not previous_seen_ids

    try:
        geos = resolve_geos(args.geo, os.environ.get("GOOGLE_TRENDS_GEOS"), args.feed)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    items: List[Dict[str, object]] = []
    errors: List[str] = []
    for geo_code in geos:
        try:
            xml_text = fetch_feed_xml(geo_feed_url(geo_code), args.timeout)
            items.extend(parse_feed(xml_text, geo_code))
        except (HTTPError, URLError, ET.ParseError) as exc:
            errors.append(f"{geo_code}: {exc}")

    if not items and errors:
        print(f"Feed fetch failed: {'; '.join(errors)}", file=sys.stderr)
        return 1

    matched = [item for item in items if is_finance_related(item)]
    new_items = [item for item in matched if item["id"] not in previous_seen_ids]
    print(build_report(items, matched, new_items, errors))

    if args.dry_run:
        return 0

    messages = build_messages(
        [] if first_run and not args.send_empty_test else new_items,
        geos,
        args.send_empty_test,
        first_run,
        errors,
    )

    if args.send_telegram:
        if not args.telegram_token or not args.telegram_chat_id:
            print(
                "Telegram is enabled but TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing.",
                file=sys.stderr,
            )
            return 2
        for message in messages:
            try:
                send_telegram(
                    args.telegram_token,
                    args.telegram_chat_id,
                    message,
                    args.timeout,
                    args.telegram_thread_id,
                )
            except (HTTPError, URLError) as exc:
                print(f"Telegram send failed: {exc}", file=sys.stderr)
                return 1

    seen_ids = merge_seen_ids(list(previous_seen_ids), [str(item["id"]) for item in matched])
    save_state(state_path, seen_ids)
    return 0


if __name__ == "__main__":
    sys.exit(main())
