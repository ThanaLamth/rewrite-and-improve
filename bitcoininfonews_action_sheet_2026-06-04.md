# BitcoinInfoNews Action Sheet

Date: 2026-06-04
Domain: `https://bitcoininfonews.com/`

This action sheet converts the audit into exact URL files and execution batches.

## Batch Order

### Batch 1: sitemap and broken-link hygiene

Do these first because they are high impact and low ambiguity.

- keep existing `noindex` on URLs listed in `bitcoininfonews_action_keep_noindex.csv`
- remove every URL in that file from sitemap outputs
- clean internal links pointing to broken targets in `bitcoininfonews_action_fix_internal_broken_targets.csv`
- review `bitcoininfonews_action_review_404_mapping.csv` for any 404 URL that should become a `301`

Counts:

- keep noindex: 3,932 URLs
- broken internal targets: 415 URLs
- 404 review list: 415 URLs

### Batch 2: index bloat reduction

Apply `noindex,follow` to deep paginated archives listed in `bitcoininfonews_action_noindex_now.csv`.

This is the cleanest way to shrink indexable archive bloat without deleting access paths.

Count:

- noindex now: 1,446 URLs

### Batch 3: duplicate consolidation

Apply `301` redirects from URLs in `bitcoininfonews_action_301_now.csv` to their mapped canonical targets.

These are the high-confidence numbered duplicates where the unsuffixed target already exists as a `200` indexable URL.

Count:

- 301 now: 296 URLs

Note:

- `bitcoininfonews_action_301_review_taxonomy.csv` is currently empty, which means no separate taxonomy duplicate set survived the high-confidence filter in this pass.

### Batch 4: content quality pruning review

Review the URLs in `bitcoininfonews_action_review_content_pruning.csv`.

These are still indexable after technical cleanup, but they match strong promo/search-first patterns such as:

- `presale`
- `best crypto to buy`
- `ROI`
- `buy now`
- `price prediction`
- `meme coin`

Count:

- review for prune/consolidate/keep: 957 URLs

Recommended decision order inside this batch:

1. consolidate obvious topic duplicates
2. deindex or retire weak sponsored/promo pages with no lasting value
3. keep only the strongest source-backed winners

## Exact Files

- `bitcoininfonews_action_301_now.csv`
- `bitcoininfonews_action_noindex_now.csv`
- `bitcoininfonews_action_keep_noindex.csv`
- `bitcoininfonews_action_keep_now.csv`
- `bitcoininfonews_action_review_content_pruning.csv`
- `bitcoininfonews_action_review_404_mapping.csv`
- `bitcoininfonews_action_fix_internal_broken_targets.csv`

## File Meanings

### `bitcoininfonews_action_301_now.csv`

Exact source-to-target redirect map for high-confidence numbered duplicates.

### `bitcoininfonews_action_noindex_now.csv`

Exact list of deep paginated archive URLs that should move to `noindex,follow`.

### `bitcoininfonews_action_keep_noindex.csv`

Exact list of URLs that should remain accessible but not indexed, such as search, author, and tag pages.

### `bitcoininfonews_action_keep_now.csv`

Current technical winner set after excluding:

- deep paginated archive URLs moved to `noindex`
- high-confidence numbered duplicates moved to `301`
- already `noindex` inventory

Count:

- keep now: 12,140 URLs

Important:

- this is a technical keep set, not a final editorial quality keep set
- use it together with `bitcoininfonews_action_review_content_pruning.csv`

### `bitcoininfonews_action_review_content_pruning.csv`

URLs that are still indexable winners technically, but need editorial review before long-term retention.

### `bitcoininfonews_action_review_404_mapping.csv`

Exact list of crawl-discovered site URLs returning `404`. Use this to decide:

- keep as `404`
- map to `301`
- remove internal links only

### `bitcoininfonews_action_fix_internal_broken_targets.csv`

Prioritized broken internal destinations with inlink counts, so dev can start from the most repeated broken targets first.

## Recommended Workflow

1. fix sitemap generation and broken internal links
2. apply `noindex` to deep pagination
3. apply `301` to numbered duplicate winners in the redirect map
4. recrawl
5. then review the 957 promo/search-first pages for prune vs consolidate vs keep

## Current Counts

- `301 now`: 296
- `noindex now`: 1,446
- `keep noindex`: 3,932
- `keep now`: 12,140
- `review content pruning`: 957
- `broken internal targets`: 415
