#!/usr/bin/env python3
import argparse
import csv
import html
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth


ROOT = Path("/home/qcweb/rewrite-and-improve")
BROKEN_TARGETS_CSV = ROOT / "bitcoininfonews_action_fix_internal_broken_targets.csv"
ALL_INLINKS_CSV = Path("/home/qcweb/bitcoininfonews/all_inlinks.csv")
INTERNAL_HTML_CSV = Path("/home/qcweb/bitcoininfonews/internal_html.csv")

WP_API_BASE = "https://bitcoininfonews.com/wp-json/wp/v2"
WP_USERNAME = "Diego Martinez"
WP_APP_PASSWORD = "Uo1P KG5l kLnW ghIj 3qPP YuFh"

STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "it",
    "its",
    "less",
    "more",
    "near",
    "new",
    "now",
    "of",
    "off",
    "on",
    "or",
    "out",
    "over",
    "set",
    "says",
    "still",
    "than",
    "the",
    "to",
    "today",
    "top",
    "under",
    "up",
    "via",
    "vs",
    "what",
    "why",
    "with",
}


@dataclass(frozen=True)
class LiveUrl:
    url: str
    slug: str
    tokens: frozenset[str]
    title: str


@dataclass
class TargetSuggestion:
    target_url: Optional[str]
    score: float
    coverage: float
    overlap: int
    method: str
    note: str


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    return path.split("/")[-1] if path else ""


def is_single_post_path(url: str) -> bool:
    parts = [p for p in urlparse(url).path.split("/") if p]
    return len(parts) == 1


def normalize_tokens(text: str) -> List[str]:
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t and t not in STOPWORDS]


def sequence_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def load_broken_targets() -> List[dict]:
    with BROKEN_TARGETS_CSV.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def load_live_urls() -> Tuple[List[LiveUrl], Dict[str, set[int]]]:
    live_urls: List[LiveUrl] = []
    inverted: Dict[str, set[int]] = defaultdict(set)

    with INTERNAL_HTML_CSV.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            url = row["Address"]
            if not url.startswith("https://bitcoininfonews.com/"):
                continue
            if row["Status Code"] != "200":
                continue
            if not is_single_post_path(url):
                continue

            slug = slug_from_url(url)
            if not slug or slug in {"feed", "amp"}:
                continue

            tokens = frozenset(normalize_tokens(slug))
            live = LiveUrl(
                url=url,
                slug=slug,
                tokens=tokens,
                title=row.get("Title 1", ""),
            )
            pos = len(live_urls)
            live_urls.append(live)
            for token in tokens:
                inverted[token].add(pos)

    return live_urls, inverted


def suggest_target(
    broken_url: str, live_urls: Sequence[LiveUrl], inverted: Dict[str, set[int]]
) -> TargetSuggestion:
    if broken_url.endswith("/cdn-cgi/l/email-protection") or "/cdn-cgi/l/email-protection" in broken_url:
        return TargetSuggestion(
            target_url=None,
            score=0.0,
            coverage=0.0,
            overlap=0,
            method="cloudflare_email_protection",
            note="Rendered by Cloudflare email protection; not present as a broken href in WP raw content.",
        )

    broken_slug = slug_from_url(broken_url)
    broken_tokens = frozenset(normalize_tokens(broken_slug))
    if not broken_tokens:
        return TargetSuggestion(
            target_url=None,
            score=0.0,
            coverage=0.0,
            overlap=0,
            method="no_tokens",
            note="Broken slug had no usable tokens.",
        )

    ranked_tokens = sorted(
        broken_tokens,
        key=lambda token: (len(inverted.get(token, set())) or 10**9, len(token) * -1, token),
    )
    selected_tokens = [token for token in ranked_tokens if len(inverted.get(token, set())) <= 1500][:4]
    if not selected_tokens:
        selected_tokens = ranked_tokens[:4]

    candidate_positions: set[int] = set()
    for token in selected_tokens:
        candidate_positions.update(inverted.get(token, set()))

    if not candidate_positions:
        return TargetSuggestion(
            target_url=None,
            score=0.0,
            coverage=0.0,
            overlap=0,
            method="no_candidate",
            note="No live single-post URL shared any meaningful token.",
        )

    best: Optional[Tuple[float, float, int, str]] = None
    for pos in candidate_positions:
        live = live_urls[pos]
        overlap = len(broken_tokens & live.tokens)
        if overlap == 0:
            continue
        coverage = overlap / max(1, len(broken_tokens))
        jaccard = overlap / len(broken_tokens | live.tokens)
        seq = sequence_ratio(broken_slug, live.slug)
        score = (0.5 * coverage) + (0.3 * jaccard) + (0.2 * seq)
        if best is None or score > best[0]:
            best = (score, coverage, overlap, live.url)

    if best is None:
        return TargetSuggestion(
            target_url=None,
            score=0.0,
            coverage=0.0,
            overlap=0,
            method="no_scored_candidate",
            note="No live candidate passed minimum overlap scoring.",
        )

    score, coverage, overlap, target_url = best
    broken_slug = slug_from_url(broken_url)
    target_slug = slug_from_url(target_url)

    if score >= 0.85 and coverage >= 0.6:
        method = "high_confidence_slug_match"
        note = "Repoint to closest live URL."
    elif score >= 0.75 and coverage >= 0.5 and sequence_ratio(broken_slug, target_slug) >= 0.55:
        method = "medium_confidence_slug_match"
        note = "Repoint candidate is reasonably close."
    else:
        return TargetSuggestion(
            target_url=None,
            score=score,
            coverage=coverage,
            overlap=overlap,
            method="unlink_only",
            note=f"Top candidate below confidence threshold: {target_url}",
        )

    return TargetSuggestion(
        target_url=target_url,
        score=score,
        coverage=coverage,
        overlap=overlap,
        method=method,
        note=note,
    )


def load_source_rows() -> List[dict]:
    broken_lookup = [row["url"] for row in load_broken_targets()]
    pattern_file = Path("/tmp/bitcoininfonews_broken_targets_patterns.txt")
    pattern_file.write_text("\n".join(broken_lookup) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            "rg",
            "-n",
            "-F",
            "-f",
            str(pattern_file),
            str(ALL_INLINKS_CSV),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    header = next(csv.reader([ALL_INLINKS_CSV.open(encoding="utf-8-sig").readline()]))
    rows: List[dict] = []
    for line in proc.stdout.splitlines():
        if not line:
            continue
        match = re.match(r"^\d+:(.*)$", line)
        if not match:
            continue
        csv_line = match.group(1)
        values = next(csv.reader([csv_line]))
        rows.append(dict(zip(header, values)))
    return rows


def build_post_id_cache(session: requests.Session, source_urls: Iterable[str]) -> Dict[str, int]:
    cache: Dict[str, int] = {}
    for source_url in sorted(set(source_urls)):
        slug = slug_from_url(source_url)
        resp = session.get(
            f"{WP_API_BASE}/posts",
            params={"slug": slug, "_fields": "id,slug"},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if data:
            cache[source_url] = data[0]["id"]
    return cache


def anchor_inner_html_regex(old_href_variants: Sequence[str]) -> re.Pattern[str]:
    escaped = "|".join(re.escape(v) for v in old_href_variants)
    return re.compile(
        rf"<a\b(?=[^>]*\bhref=(['\"])(?:{escaped})\1)[^>]*>(.*?)</a>",
        flags=re.IGNORECASE | re.DOTALL,
    )


def replace_link_href(content: str, old_href_variants: Sequence[str], new_href: str) -> Tuple[str, int]:
    total = 0
    updated = content
    for old in old_href_variants:
        pattern = re.compile(
            rf"(<a\b[^>]*\bhref=)(['\"]){re.escape(old)}\2",
            flags=re.IGNORECASE,
        )
        updated, count = pattern.subn(rf"\1\2{new_href}\2", updated)
        total += count
    return updated, total


def unlink_anchor(content: str, old_href_variants: Sequence[str]) -> Tuple[str, int]:
    pattern = anchor_inner_html_regex(old_href_variants)
    updated, count = pattern.subn(lambda m: m.group(2), content)
    return updated, count


def count_href_matches(content: str, href_variants: Sequence[str]) -> int:
    escaped = "|".join(re.escape(v) for v in href_variants)
    pattern = re.compile(
        rf"<a\b[^>]*\bhref=(['\"])(?:{escaped})\1",
        flags=re.IGNORECASE,
    )
    return len(pattern.findall(content))


def old_href_variants(url: str) -> List[str]:
    parsed = urlparse(url)
    path = parsed.path or "/"
    no_trailing = path[:-1] if path.endswith("/") else path
    variants = {
        url,
        path,
        no_trailing,
        f"https://bitcoininfonews.com{path}",
        f"https://bitcoininfonews.com{no_trailing}",
    }
    return [v for v in variants if v]


def write_csv(path: Path, rows: Sequence[dict], fieldnames: Sequence[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_outputs() -> Tuple[Path, Path, Path, List[dict], List[dict]]:
    broken_targets = load_broken_targets()
    live_urls, inverted = load_live_urls()
    source_rows = load_source_rows()

    suggestions = {row["url"]: suggest_target(row["url"], live_urls, inverted) for row in broken_targets}
    target_inlinks = {row["url"]: int(row["inlinks"]) for row in broken_targets}

    detailed_rows: List[dict] = []
    summary_counter: Dict[str, Counter] = defaultdict(Counter)
    unique_targets_by_source: Dict[str, set[str]] = defaultdict(set)

    for row in source_rows:
        broken_target = row["Destination"]
        suggestion = suggestions[broken_target]
        source_url = row["Source"]
        action = (
            "replace_link_target"
            if suggestion.target_url
            else "skip_cloudflare_email_protection"
            if suggestion.method == "cloudflare_email_protection"
            else "unlink_keep_anchor_text"
        )

        detailed_rows.append(
            {
                "source_url": source_url,
                "broken_target_url": broken_target,
                "target_inlinks_aggregate": target_inlinks[broken_target],
                "anchor": row["Anchor"],
                "link_type": row["Type"],
                "position": row["Link Position"],
                "xpath": row["Link Path"],
                "current_target_status": row["Status Code"],
                "recommended_action": action,
                "suggested_target": suggestion.target_url or "",
                "confidence_score": f"{suggestion.score:.3f}",
                "coverage": f"{suggestion.coverage:.3f}",
                "match_method": suggestion.method,
                "notes": suggestion.note,
            }
        )

        summary_counter[source_url]["broken_link_occurrences"] += 1
        if action == "replace_link_target":
            summary_counter[source_url]["replace_link_target"] += 1
        elif action == "unlink_keep_anchor_text":
            summary_counter[source_url]["unlink_keep_anchor_text"] += 1
        else:
            summary_counter[source_url]["skip_cloudflare_email_protection"] += 1
        unique_targets_by_source[source_url].add(broken_target)

    summary_rows: List[dict] = []
    for source_url, counter in summary_counter.items():
        priority = "priority_1" if counter["broken_link_occurrences"] >= 4 else "priority_2" if counter["broken_link_occurrences"] >= 2 else "priority_3"
        summary_rows.append(
            {
                "source_url": source_url,
                "broken_link_occurrences": counter["broken_link_occurrences"],
                "unique_broken_targets": len(unique_targets_by_source[source_url]),
                "priority_batch": priority,
                "replace_link_target": counter["replace_link_target"],
                "unlink_keep_anchor_text": counter["unlink_keep_anchor_text"],
                "skip_cloudflare_email_protection": counter["skip_cloudflare_email_protection"],
            }
        )

    summary_rows.sort(
        key=lambda row: (
            {"priority_1": 0, "priority_2": 1, "priority_3": 2}[row["priority_batch"]],
            -int(row["broken_link_occurrences"]),
            row["source_url"],
        )
    )

    date = time.strftime("%Y-%m-%d")
    detail_path = ROOT / f"bitcoininfonews_internal_broken_link_source_rows_{date}.csv"
    summary_path = ROOT / f"bitcoininfonews_internal_broken_link_source_summary_{date}.csv"
    memo_path = ROOT / f"bitcoininfonews_internal_broken_link_fix_memo_{date}.md"

    write_csv(
        detail_path,
        detailed_rows,
        [
            "source_url",
            "broken_target_url",
            "target_inlinks_aggregate",
            "anchor",
            "link_type",
            "position",
            "xpath",
            "current_target_status",
            "recommended_action",
            "suggested_target",
            "confidence_score",
            "coverage",
            "match_method",
            "notes",
        ],
    )
    write_csv(
        summary_path,
        summary_rows,
        [
            "source_url",
            "broken_link_occurrences",
            "unique_broken_targets",
            "priority_batch",
            "replace_link_target",
            "unlink_keep_anchor_text",
            "skip_cloudflare_email_protection",
        ],
    )

    replace_count = sum(1 for row in detailed_rows if row["recommended_action"] == "replace_link_target")
    unlink_count = sum(1 for row in detailed_rows if row["recommended_action"] == "unlink_keep_anchor_text")
    skip_count = sum(1 for row in detailed_rows if row["recommended_action"] == "skip_cloudflare_email_protection")

    with memo_path.open("w", encoding="utf-8") as fh:
        fh.write("# BitcoinInfoNews internal broken link fix memo\n\n")
        fh.write(f"- Broken targets in input sheet: {len(broken_targets)}\n")
        fh.write(f"- Broken-link occurrences in source pages: {len(detailed_rows)}\n")
        fh.write(f"- Unique source pages affected: {len(summary_rows)}\n")
        fh.write(f"- Replace target actions: {replace_count}\n")
        fh.write(f"- Unlink actions: {unlink_count}\n")
        fh.write(f"- Cloudflare email-protection rows skipped from content edits: {skip_count}\n\n")
        fh.write("## Execution rule\n\n")
        fh.write("- `replace_link_target`: switch broken href to the closest live article URL.\n")
        fh.write("- `unlink_keep_anchor_text`: remove the hyperlink but keep its visible text.\n")
        fh.write("- `skip_cloudflare_email_protection`: email-protection links are rendered at edge level and were not found as broken hrefs in WP raw content.\n")

    return detail_path, summary_path, memo_path, detailed_rows, summary_rows


def apply_live_updates(detailed_rows: Sequence[dict], limit_sources: Optional[int] = None) -> None:
    session = requests.Session()
    session.auth = HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD)

    actionable = [
        row
        for row in detailed_rows
        if row["recommended_action"] in {"replace_link_target", "unlink_keep_anchor_text"}
    ]
    by_source: Dict[str, List[dict]] = defaultdict(list)
    for row in actionable:
        by_source[row["source_url"]].append(row)

    source_urls = sorted(by_source)
    if limit_sources is not None:
        source_urls = source_urls[:limit_sources]

    id_cache = build_post_id_cache(session, source_urls)

    results = []
    for source_url in source_urls:
        post_id = id_cache.get(source_url)
        if not post_id:
            results.append({"source_url": source_url, "status": "missing_post_id", "changes": 0})
            continue

        resp = session.get(f"{WP_API_BASE}/posts/{post_id}", params={"context": "edit"}, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        raw = payload["content"]["raw"]
        updated = raw
        change_count = 0

        for row in by_source[source_url]:
            old_variants = old_href_variants(row["broken_target_url"])
            if row["recommended_action"] == "replace_link_target":
                updated, count = replace_link_href(updated, old_variants, row["suggested_target"])
            else:
                updated, count = unlink_anchor(updated, old_variants)
            change_count += count

        if updated == raw:
            results.append({"source_url": source_url, "status": "no_change", "changes": 0})
            continue

        update_resp = session.post(
            f"{WP_API_BASE}/posts/{post_id}",
            json={"content": updated},
            timeout=30,
        )
        update_resp.raise_for_status()
        results.append({"source_url": source_url, "status": "updated", "changes": change_count})
        time.sleep(0.2)

    print(json.dumps(results, indent=2))


def verify_live_updates(detailed_rows: Sequence[dict]) -> Path:
    session = requests.Session()
    session.auth = HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD)

    actionable = [
        row
        for row in detailed_rows
        if row["recommended_action"] in {"replace_link_target", "unlink_keep_anchor_text"}
    ]
    by_source: Dict[str, List[dict]] = defaultdict(list)
    for row in actionable:
        by_source[row["source_url"]].append(row)

    id_cache = build_post_id_cache(session, by_source.keys())
    verify_rows: List[dict] = []

    for source_url in sorted(by_source):
        post_id = id_cache.get(source_url)
        if not post_id:
            verify_rows.append(
                {
                    "source_url": source_url,
                    "post_lookup_status": "missing_post_id",
                    "action_rows": len(by_source[source_url]),
                    "remaining_old_href_hits": "",
                    "expected_new_href_hits": "",
                }
            )
            continue

        resp = session.get(f"{WP_API_BASE}/posts/{post_id}", params={"context": "edit"}, timeout=30)
        resp.raise_for_status()
        raw = resp.json()["content"]["raw"]

        remaining_old = 0
        expected_new = 0
        for row in by_source[source_url]:
            old_hits = count_href_matches(raw, old_href_variants(row["broken_target_url"]))
            remaining_old += old_hits
            if row["recommended_action"] == "replace_link_target":
                expected_new += count_href_matches(raw, [row["suggested_target"]])

        verify_rows.append(
            {
                "source_url": source_url,
                "post_lookup_status": "ok",
                "action_rows": len(by_source[source_url]),
                "remaining_old_href_hits": remaining_old,
                "expected_new_href_hits": expected_new,
            }
        )

    date = time.strftime("%Y-%m-%d")
    verify_path = ROOT / f"bitcoininfonews_internal_broken_link_verify_{date}.csv"
    write_csv(
        verify_path,
        verify_rows,
        [
            "source_url",
            "post_lookup_status",
            "action_rows",
            "remaining_old_href_hits",
            "expected_new_href_hits",
        ],
    )
    return verify_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply live WP content updates.")
    parser.add_argument("--verify", action="store_true", help="Verify remaining old href hits after edits.")
    parser.add_argument("--limit-sources", type=int, default=None, help="Apply to first N source URLs only.")
    args = parser.parse_args()

    detail_path, summary_path, memo_path, detailed_rows, summary_rows = generate_outputs()
    print(detail_path)
    print(summary_path)
    print(memo_path)
    print(f"detailed_rows={len(detailed_rows)} summary_rows={len(summary_rows)}")

    if args.apply:
        apply_live_updates(detailed_rows, limit_sources=args.limit_sources)
    if args.verify:
        verify_path = verify_live_updates(detailed_rows)
        print(verify_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
