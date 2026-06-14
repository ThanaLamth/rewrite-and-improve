# BitcoinInfoNews Remaining Indexability Actions - 2026-06-12

## Batch 1: content URLs to noindex now
- File: `bitcoininfonews_action_noindex_content_now_2026-06-12.csv`
- URLs: 97
- Evidence: all 97 are still indexable; 97/97 have 0 clicks; only 6/97 have any impressions.
- Action: noindex at post level.

## Batch 2: keep indexed traffic exception
- File: `bitcoininfonews_action_keep_index_content_exception_2026-06-12.csv`
- URLs: 1
- URL: `https://bitcoininfonews.com/central-african-republic-national-meme-coin/`
- Evidence: 32 clicks, 44 impressions, avg position 1.48; currently 200 indexable.
- Action: keep indexed.

## Batch 3: utility/taxonomy cleanup
- File: `bitcoininfonews_action_utility_taxonomy_indexability_final_2026-06-12.csv`
- Immediate noindex file: `bitcoininfonews_action_noindex_utility_now_2026-06-12.csv` (7 URLs)
- Keep indexed file: `bitcoininfonews_action_keep_index_hub_now_2026-06-12.csv` (1 URL)
- Review slug collisions: `bitcoininfonews_action_review_slug_collisions_2026-06-12.csv` (2 URLs)
- Already resolved 404/noindex: `bitcoininfonews_action_already_404_no_action_2026-06-12.csv` (8 URLs)

## Key live findings
- `news/` is a live 200 indexable hub with self-canonical.
- `press-release/`, `sponsored-articles/`, `cmc/`, `other/`, `others/`, `mining/`, `top-project/`, `uncategorized/` already return 404 with `follow, noindex`.
- `millionaire/` 301 redirects by WordPress to a single article.
- `blockchain-events/` 301 redirects by WordPress to a single article.
