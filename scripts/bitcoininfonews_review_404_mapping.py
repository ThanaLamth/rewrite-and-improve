#!/usr/bin/env python3
import csv
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence
from urllib.parse import parse_qs, urlparse

import requests


ROOT = Path("/home/qcweb/rewrite-and-improve")
REVIEW_404 = ROOT / "bitcoininfonews_action_review_404_mapping.csv"
KEEP_NOW = ROOT / "bitcoininfonews_action_keep_now.csv"
ACTION_301_NOW = ROOT / "bitcoininfonews_action_301_now.csv"
INTERNAL_HTML = Path("/home/qcweb/bitcoininfonews/internal_html.csv")

UA = "Mozilla/5.0 (compatible; Codex 404 mapping audit)"
STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "it",
    "its",
    "new",
    "of",
    "on",
    "or",
    "out",
    "the",
    "to",
    "up",
    "with",
}


@dataclass(frozen=True)
class Candidate:
    url: str
    slug: str
    title: str
    tokens: frozenset[str]


def slug_from_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if path:
        return path.split("/")[-1]
    query = parse_qs(parsed.query)
    if "p" in query and query["p"]:
        return f"p-{query['p'][0]}"
    return ""


def tokenize(text: str) -> List[str]:
    out = []
    for token in "".join(ch if ch.isalnum() else " " for ch in text.lower()).split():
        if token and token not in STOPWORDS:
            out.append(token)
    return out


def is_single_post_like(url: str) -> bool:
    path = urlparse(url).path
    parts = [part for part in path.split("/") if part]
    return len(parts) <= 1


def load_review_rows() -> List[dict]:
    with REVIEW_404.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def load_candidates() -> List[Candidate]:
    keep_now_urls = set()
    with KEEP_NOW.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            keep_now_urls.add(row["url"])

    title_lookup: Dict[str, str] = {}
    with INTERNAL_HTML.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            title_lookup[row["Address"]] = row.get("Title 1", "")

    candidates: List[Candidate] = []
    seen = set()

    for url in sorted(keep_now_urls):
        if url in seen:
            continue
        seen.add(url)
        slug = slug_from_url(url)
        title = title_lookup.get(url, "")
        candidates.append(
            Candidate(
                url=url,
                slug=slug,
                title=title,
                tokens=frozenset(tokenize(slug)),
            )
        )

    with ACTION_301_NOW.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            target_url = row["target_url"]
            if target_url in seen:
                continue
            seen.add(target_url)
            slug = slug_from_url(target_url)
            title = title_lookup.get(target_url, row.get("target_title", ""))
            candidates.append(
                Candidate(
                    url=target_url,
                    slug=slug,
                    title=title,
                    tokens=frozenset(tokenize(slug)),
                )
            )

    return candidates


def build_inverted_index(candidates: Sequence[Candidate]) -> Dict[str, set[int]]:
    inv: Dict[str, set[int]] = defaultdict(set)
    for idx, candidate in enumerate(candidates):
        for token in candidate.tokens:
            inv[token].add(idx)
    return inv


def seq_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def candidate_score(broken_url: str, candidate: Candidate) -> tuple[float, float, float, float]:
    broken_slug = slug_from_url(broken_url)
    broken_tokens = frozenset(tokenize(broken_slug))
    if not broken_tokens:
        return 0.0, 0.0, 0.0, 0.0

    overlap = len(broken_tokens & candidate.tokens)
    if overlap == 0:
        return 0.0, 0.0, 0.0, 0.0

    coverage = overlap / len(broken_tokens)
    jaccard = overlap / len(broken_tokens | candidate.tokens)
    seq = seq_ratio(broken_slug, candidate.slug)
    score = (0.5 * coverage) + (0.3 * jaccard) + (0.2 * seq)
    return score, coverage, jaccard, seq


def suggest_target(
    broken_url: str,
    candidates: Sequence[Candidate],
    inverted: Dict[str, set[int]],
) -> dict:
    broken_slug = slug_from_url(broken_url)
    broken_tokens = frozenset(tokenize(broken_slug))
    if not broken_tokens:
        return {
            "target_url": "",
            "score": 0.0,
            "coverage": 0.0,
            "jaccard": 0.0,
            "seq": 0.0,
            "decision": "keep_404_manual_review",
            "note": "No usable slug tokens.",
        }

    ranked_tokens = sorted(
        broken_tokens,
        key=lambda token: (len(inverted.get(token, set())) or 10**9, -len(token), token),
    )
    selected_tokens = [t for t in ranked_tokens if len(inverted.get(t, set())) <= 1500][:5]
    if not selected_tokens:
        selected_tokens = ranked_tokens[:5]

    candidate_ids = set()
    for token in selected_tokens:
        candidate_ids.update(inverted.get(token, set()))

    scored = []
    for idx in candidate_ids:
        candidate = candidates[idx]
        score, coverage, jaccard, seq = candidate_score(broken_url, candidate)
        if score == 0:
            continue
        scored.append((score, coverage, jaccard, seq, candidate))

    scored.sort(key=lambda item: item[:4], reverse=True)
    if not scored:
        return {
            "target_url": "",
            "score": 0.0,
            "coverage": 0.0,
            "jaccard": 0.0,
            "seq": 0.0,
            "decision": "keep_404_no_candidate",
            "note": "No live winner candidate shared enough tokens.",
        }

    top = scored[0]
    score, coverage, jaccard, seq, candidate = top
    target_url = candidate.url

    if score >= 0.90 and coverage >= 0.80:
        decision = "301_now_high_confidence"
        note = "Very close slug variant to current winner."
    elif score >= 0.82 and coverage >= 0.65 and seq >= 0.55:
        decision = "301_now_medium_confidence"
        note = "Close enough to current winner for direct 301."
    elif score >= 0.72 and coverage >= 0.55:
        decision = "manual_review"
        note = "Likely match, but keep manual review because similarity is not strong enough."
    else:
        decision = "keep_404"
        note = f"Closest winner still weak: {target_url}"

    return {
        "target_url": target_url,
        "score": score,
        "coverage": coverage,
        "jaccard": jaccard,
        "seq": seq,
        "decision": decision,
        "note": note,
    }


def fetch_status(url: str) -> dict:
    session = requests.Session()
    session.headers["User-Agent"] = UA
    try:
        response = session.get(url, allow_redirects=False, timeout=20)
        return {
            "url": url,
            "status_code": response.status_code,
            "location": response.headers.get("Location", ""),
            "redirect_by": response.headers.get("x-redirect-by", ""),
        }
    except Exception as exc:
        return {
            "url": url,
            "status_code": 0,
            "location": "",
            "redirect_by": f"ERROR: {exc}",
        }


def fetch_all_statuses(urls: Iterable[str]) -> Dict[str, dict]:
    results: Dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=16) as pool:
        future_map = {pool.submit(fetch_status, url): url for url in urls}
        for future in as_completed(future_map):
            payload = future.result()
            results[payload["url"]] = payload
    return results


def write_csv(path: Path, rows: List[dict], fieldnames: Sequence[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    review_rows = load_review_rows()
    candidates = load_candidates()
    inverted = build_inverted_index(candidates)
    statuses = fetch_all_statuses(row["url"] for row in review_rows)

    review_detail_rows: List[dict] = []
    action_301_rows: List[dict] = []
    keep_404_rows: List[dict] = []
    manual_rows: List[dict] = []

    for row in review_rows:
        url = row["url"]
        status = statuses[url]
        suggestion = suggest_target(url, candidates, inverted)
        broken_slug = slug_from_url(url)

        review_detail = {
            "source_404_url": url,
            "broken_slug": broken_slug,
            "live_status_code": status["status_code"],
            "live_location": status["location"],
            "redirect_by": status["redirect_by"],
            "suggested_target_url": suggestion["target_url"],
            "score": f"{suggestion['score']:.3f}",
            "coverage": f"{suggestion['coverage']:.3f}",
            "jaccard": f"{suggestion['jaccard']:.3f}",
            "sequence_ratio": f"{suggestion['seq']:.3f}",
            "decision": suggestion["decision"],
            "note": suggestion["note"],
        }
        review_detail_rows.append(review_detail)

        if status["status_code"] in {301, 302, 307, 308}:
            keep_404_rows.append(
                {
                    "url": url,
                    "reason": f"already redirects live to {status['location']}",
                    "live_status_code": status["status_code"],
                    "live_location": status["location"],
                    "decision": "leave_as_is",
                }
            )
            continue

        if suggestion["decision"].startswith("301_now"):
            action_301_rows.append(
                {
                    "source_url": url,
                    "target_url": suggestion["target_url"],
                    "source_title": row.get("title", ""),
                    "target_title": "",
                    "reason": suggestion["note"],
                    "batch": "batch_1_internal_link_cleanup_and_404_mapping",
                    "score": f"{suggestion['score']:.3f}",
                }
            )
        elif suggestion["decision"] in {"keep_404", "keep_404_no_candidate"}:
            keep_404_rows.append(
                {
                    "url": url,
                    "reason": suggestion["note"],
                    "live_status_code": status["status_code"],
                    "live_location": status["location"],
                    "decision": suggestion["decision"],
                }
            )
        else:
            manual_rows.append(
                {
                    "url": url,
                    "suggested_target_url": suggestion["target_url"],
                    "score": f"{suggestion['score']:.3f}",
                    "coverage": f"{suggestion['coverage']:.3f}",
                    "sequence_ratio": f"{suggestion['seq']:.3f}",
                    "reason": suggestion["note"],
                    "live_status_code": status["status_code"],
                    "live_location": status["location"],
                }
            )

    detail_path = ROOT / "bitcoininfonews_404_mapping_review_detail_2026-06-09.csv"
    action_301_path = ROOT / "bitcoininfonews_action_301_now_from_404_review_2026-06-09.csv"
    rankmath_import_path = ROOT / "bitcoininfonews_rankmath_301_from_404_review_2026-06-09.csv"
    keep_404_path = ROOT / "bitcoininfonews_action_keep_404_2026-06-09.csv"
    manual_path = ROOT / "bitcoininfonews_action_review_404_manual_2026-06-09.csv"
    summary_path = ROOT / "bitcoininfonews_404_mapping_summary_2026-06-09.md"

    write_csv(
        detail_path,
        review_detail_rows,
        [
            "source_404_url",
            "broken_slug",
            "live_status_code",
            "live_location",
            "redirect_by",
            "suggested_target_url",
            "score",
            "coverage",
            "jaccard",
            "sequence_ratio",
            "decision",
            "note",
        ],
    )
    write_csv(
        action_301_path,
        action_301_rows,
        ["source_url", "target_url", "source_title", "target_title", "reason", "batch", "score"],
    )
    rankmath_rows = [
        {
            "source": urlparse(row["source_url"]).path.lstrip("/") + (("?" + urlparse(row["source_url"]).query) if urlparse(row["source_url"]).query else ""),
            "destination": row["target_url"],
            "matching": "exact",
            "type": "301",
            "status": "active",
        }
        for row in action_301_rows
    ]
    write_csv(
        rankmath_import_path,
        rankmath_rows,
        ["source", "destination", "matching", "type", "status"],
    )
    write_csv(
        keep_404_path,
        keep_404_rows,
        ["url", "reason", "live_status_code", "live_location", "decision"],
    )
    write_csv(
        manual_path,
        manual_rows,
        ["url", "suggested_target_url", "score", "coverage", "sequence_ratio", "reason", "live_status_code", "live_location"],
    )

    status_counts = Counter(str(statuses[row["url"]]["status_code"]) for row in review_rows)
    decision_counts = Counter(row["decision"] for row in review_detail_rows)
    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write("# BitcoinInfoNews 404 mapping summary\n\n")
        fh.write(f"- Reviewed URLs: {len(review_rows)}\n")
        fh.write(f"- Live status counts: {dict(status_counts)}\n")
        fh.write(f"- Decision counts: {dict(decision_counts)}\n")
        fh.write(f"- 301-now suggestions: {len(action_301_rows)}\n")
        fh.write(f"- Keep-404 suggestions: {len(keep_404_rows)}\n")
        fh.write(f"- Manual-review suggestions: {len(manual_rows)}\n")

    print(detail_path)
    print(action_301_path)
    print(rankmath_import_path)
    print(keep_404_path)
    print(manual_path)
    print(summary_path)
    print("status_counts", dict(status_counts))
    print("decision_counts", dict(decision_counts))
    print("action_301_rows", len(action_301_rows))
    print("keep_404_rows", len(keep_404_rows))
    print("manual_rows", len(manual_rows))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
