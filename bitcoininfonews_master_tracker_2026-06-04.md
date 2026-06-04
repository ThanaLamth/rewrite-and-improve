# BitcoinInfoNews Master Tracker

Date: 2026-06-04
Domain: `https://bitcoininfonews.com/`

This is the single entry point for the BitcoinInfoNews audit work.

## Core Files

- Audit report: `bitcoininfonews_audit_2026-06-04.md`
- Action sheet: `bitcoininfonews_action_sheet_2026-06-04.md`

## Execution Order

### Batch 1

Goal: clean sitemap-derived noise and internal broken signals first.

1. Keep existing `noindex` and remove these URLs from sitemaps
   File: `bitcoininfonews_action_keep_noindex.csv`
   Count: 3,932

2. Fix broken internal targets
   File: `bitcoininfonews_action_fix_internal_broken_targets.csv`
   Count: 415

3. Review 404 URLs that may deserve redirect mapping
   File: `bitcoininfonews_action_review_404_mapping.csv`
   Count: 415

### Batch 2

Goal: reduce index bloat from deep archive pagination.

1. Apply `noindex,follow` to deep paginated archives
   File: `bitcoininfonews_action_noindex_now.csv`
   Count: 1,446

### Batch 3

Goal: consolidate numbered duplicates into preferred canonical winners.

1. Apply `301` redirects for high-confidence duplicate winners
   File: `bitcoininfonews_action_301_now.csv`
   Count: 296

2. Taxonomy duplicate review
   File: `bitcoininfonews_action_301_review_taxonomy.csv`
   Count: 0

### Batch 4

Goal: review search-first promo inventory after technical cleanup.

1. Review prune vs consolidate vs keep decisions
   File: `bitcoininfonews_action_review_content_pruning.csv`
   Count: 957

### Batch 5

Goal: review thin utility pages and taxonomy hubs that may not deserve indexation.

1. Review utility and taxonomy indexables
   File: `bitcoininfonews_action_review_utility_and_taxonomy_indexables.csv`
   Count: 18

## Recommended Decision Rules

### `301`

Use `301` when:

- the source URL is a duplicate or replaced page
- a clear preferred winner already exists
- the target satisfies the same or better intent

### `noindex,follow`

Use `noindex,follow` when:

- the page should stay accessible
- the page is archive, search, author, or low-value pagination
- the page does not need to rank directly

### Keep Indexed

Keep indexed when:

- the page is a preferred canonical winner
- the page has real standalone search value
- the page is not duplicated or excessively promotional

### Manual Review

Use manual review when:

- a 404 might need redirect mapping
- a sponsored or promo page might still deserve to stay live
- a utility or taxonomy page may need more content before staying indexed

## Work Sequence

1. Finish Batch 1 completely.
2. Recrawl the site.
3. Apply Batch 2 and Batch 3.
4. Recrawl again.
5. Only then start Batch 4 and Batch 5 editorial review.

## Deliverable Checklist

- sitemap contains only canonical indexable URLs
- internal links stop pointing to 301 and 404 targets
- deep pagination is noindexed if not worth ranking
- numbered duplicate URLs are consolidated
- weak promo inventory is pruned or merged
- utility and taxonomy hubs are intentionally indexed or intentionally noindexed
