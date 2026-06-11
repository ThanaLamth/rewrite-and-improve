# TheCCPress Task 8: Tag Archive Surface

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

- `review_keep`: `55`
- `merge_candidate`: `6`
- `review_merge_or_drop`: `431`
- `drop_or_leave_noindex`: `2720`

## Recommended Next Step

Do not try to “fix” all tags at once.

Start with:

1. merge the obvious synonym pairs
2. stop new one-off tag creation in editorial workflow
3. leave the long tail noindexed for now unless the rebuild or taxonomy overhaul is already scheduled

## Practical Execution Steps

### Phase 1: Freeze New Tag Sprawl

Do this first because it stops the problem from getting worse.

1. tell editors not to create new one-off tags for single articles
2. only allow tags when they are expected to be reused across multiple articles
3. keep category assignment as the primary taxonomy and treat tags as optional

### Phase 2: Merge the Clear Synonyms

Start with the low-risk merge pairs from the decision sheet:

1. `btc -> bitcoin`
2. `eth -> ethereum`
3. `ripple -> xrp`
4. `ripple-xrp -> xrp`
5. `crypto -> cryptocurrency`
6. `cryptocurrency-exchange -> crypto-exchange`

Practical handling:

1. move posts from the weaker tag to the keeper tag
2. if the weaker tag becomes empty, delete it
3. keep the archive `noindex` unless there is a deliberate reason to change the tag strategy later

### Phase 2 Status On 2026-06-11

These six merges were executed live via WordPress REST and rechecked by slug lookup afterward.

Verified outcomes:

1. `btc -> bitcoin`
   `btc` no longer exists, `bitcoin` now has `117` posts
2. `eth -> ethereum`
   `eth` no longer exists, `ethereum` now has `71` posts
3. `ripple -> xrp`
   `ripple` no longer exists, `xrp` rose to `74` after this step
4. `ripple-xrp -> xrp`
   `ripple-xrp` no longer exists, `xrp` now has `92` posts
5. `crypto -> cryptocurrency`
   `crypto` no longer exists, `cryptocurrency` now has `307` posts
6. `cryptocurrency-exchange -> crypto-exchange`
   `cryptocurrency-exchange` no longer exists, `crypto-exchange` now has `49` posts

Detailed execution log:

- [`/home/qcweb/rewrite-and-improve/theccpress_tag_merge_results_2026-06-11.csv`](/home/qcweb/rewrite-and-improve/theccpress_tag_merge_results_2026-06-11.csv)

### Phase 3: Review the Small Keep Set

Use the `review_keep` rows as the only candidate set worth preserving as genuine editorial tags.

Examples with stronger support:

1. `cryptocurrency`
2. `blockchain`
3. `bitcoin`
4. `ethereum`
5. `xrp`
6. `altcoins`
7. `crypto-exchange`

For each one:

1. confirm it is attached to multiple real editorial stories
2. confirm it is not just a label clone of a category
3. keep it only if there is a real newsroom use case

### Phase 4: Leave the Long Tail Noindexed

For the `2720` rows labeled `drop_or_leave_noindex`:

1. do not spend time manually fixing each tag
2. leave them `noindex`
3. optionally delete them only when a broader taxonomy cleanup is already happening

This long tail mostly consists of:

1. single-use tags
2. promo or campaign tags
3. weak descriptive fragments
4. administrative labels like `featured` or `sponsored`

### Phase 5: Optional Bulk Cleanup Later

If you later decide to clean tags more aggressively:

1. export all tags from WordPress
2. map each tag to one of:
   - keep
   - merge
   - delete
3. reassign posts in bulk
4. delete empty tags

### Best Practical Rule for Now

For the current WordPress site, the safest move is:

1. keep tags `noindex`
2. merge only the obvious synonym pairs
3. stop new one-off tag creation
4. defer deep tag pruning until the broader rebuild or taxonomy project

## Final Phase 3 Decision

Do not preserve all `55` rows that were initially flagged as `review_keep`.

That bucket was only a shortlist for review, not a final keep set.

The practical final decision is to keep a much smaller editorial tag core.

### Keep Core Now

These are the tags worth keeping as the active newsroom tag vocabulary for the current site:

1. `cryptocurrency`
2. `blockchain`
3. `bitcoin`
4. `ethereum`
5. `xrp`
6. `altcoins`
7. `crypto-exchange`
8. `mining`
9. `wallet`
10. `smart-contracts`
11. `coinbase`
12. `binance`

Why these stay:

1. they are broad recurring editorial topics or major recurring entities
2. they are understandable to readers
3. they can span multiple categories and article types without becoming one-off clutter

### Optional Keep Only If Editorial Reuses Them Often

These can stay only if the newsroom genuinely reuses them across many non-promo stories:

1. `cardano`
2. `litecoin`
3. `stellar`
4. `monero`
5. `tron`
6. `sec`

If editorial does not actively use them as recurring cross-story labels, leave them noindex and stop assigning them going forward.

### Do Not Treat These As Keepers

Even though some of these landed in the initial `review_keep` bucket, they should not be part of the final active tag core:

1. `latest-news`
2. `altcoin-news`
3. `exchange`
4. `cryptocurrencies`
5. `technology`
6. `token`
7. `crypto-trading`
8. `investment`
9. `partnership`
10. `media`
11. `event`
12. `ico`
13. `blockdag`
14. `trollercat`
15. `trollercat-com`

Why these should not be kept:

1. they duplicate category or section intent
2. they are too vague to be useful taxonomy labels
3. they are brand or promo-specific clutter
4. they do not justify a stable long-term tag vocabulary

### Practical Rule For Editors

From now on, a new tag should be allowed only if all three are true:

1. it will be reused across multiple future stories
2. it is not already covered by a category
3. it is not just a coin ticker, promo phrase, or campaign label
