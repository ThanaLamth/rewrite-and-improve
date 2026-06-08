# TheCCPress Taxonomy Migration Plan

Date: 2026-06-08
Domain: `https://theccpress.com/`
Status: `plan approved for phased execution`

## Core Decision

Do **not** mass-recategorize CCPress immediately.

The site should follow this order:

1. fix URL architecture conflicts first
2. freeze current taxonomy growth
3. introduce a hybrid taxonomy model
4. pilot recategorization on controlled article sets
5. expand only after recrawl and GSC validation

This is the lowest-risk path because the site currently has:

- archive canonical vs redirect conflicts
- global internal links to redirecting archive URLs
- real internal `404` waste
- unstable crawl behavior in both local crawl and GSC Crawl Stats

If recategorization is rolled out before those issues are stabilized, it will be difficult to separate:

- existing indexation failure
- migration bugs
- post-move crawl instability

## Recommended Model

Do **not** use the proposed narrative layer as the only primary category structure.

Use a **hybrid model** instead:

### 1. Primary SEO Categories

These categories should carry the default archive, internal linking, and indexation responsibility.

- `bitcoin-news`
- `altcoin-news`
- `regulation` `new`
- `companies` `new`
- `people` `new`
- `investigations` `new`
- `learn-crypto`
- `press-releases`
- `sponsored-articles`

### 2. Narrative / Editorial Hub Layer

These should be built as editorial hubs, series pages, or controlled secondary taxonomies. They should not replace the full sitewide primary classification by themselves.

- `/stories/market-drama/`
- `/stories/company-sagas/`
- `/stories/project-rise-fall/`
- `/conflicts/regulation/`
- `/conflicts/company/`
- `/conflicts/ideology/`
- `/people/founders/`
- `/people/influencers/`
- `/people/institutions/`
- `/power/exchanges/`
- `/power/vcs/`
- `/power/regulators/`
- `/investigations/fraud/`
- `/investigations/collapse/`
- `/investigations/controversy/`

### Why This Model

The narrative layer is strong for editorial identity, but weak as a full replacement for all article categorization because:

- categories such as `power`, `conflicts`, and `stories` are too abstract for many news articles
- one article can fit multiple narrative buckets at once
- the current archive inventory is too large to remap cleanly into those buckets without ambiguity

The hybrid model preserves:

- search clarity
- cleaner archive logic
- a stronger editorial voice

## Phase Plan

## Phase 0. Freeze

Duration: immediate

Rules:

- do not add new top-level categories during the URL repair phase
- stop creating new utility categories such as `pin-post`, `mining`, `binance`, and `top-picks`
- stop adding fresh posts into weak legacy buckets unless there is a clear business reason

Deliverables:

- taxonomy freeze note for editors
- category creation lock in workflow if possible

## Phase 1. Repair URL Architecture First

Duration: first execution phase

Goal:

- make archive URLs send one clean canonical signal

Rules:

- keep `/category/...` as the temporary canonical archive structure for the repair phase
- update all conflicted category pages so they self-canonicalize to their own `/category/...` URL
- make pretty archive variants redirect to the canonical `/category/...` URL
- update menu and template links so they point directly to final archive destinations

Priority groups:

- `category/latest-news/`
- `category/latest-news/bitcoin-news/`
- `category/latest-news/press-release/`
- `category/altcoin-news/`
- `category/altcoin-news/ethereum/`
- `category/crypto-101/`
- `category/blockchain-events/`
- `category/learn-crypto/blockchain-technology/`

Exit criteria:

- no category archive canonicalizes to a URL that returns `301` or `404`
- template links no longer hit archive redirects
- recrawl confirms major reduction in internal `301` archive links

## Phase 2. Rationalize Current Primary Categories

Duration: after Phase 1 recrawl

Keep and strengthen:

- `bitcoin-news`
- `altcoin-news`
- `learn-crypto`
- `press-releases`
- `sponsored-articles`

Demote or retire over time:

- `latest-news`
- `news`
- `cmc`
- `top-picks`
- `binance`
- `pin-post`
- `mining`

Merge or review low-value subcategories:

- `analysis`
- `blockchain-news`
- `cryptocurrencies`
- `services`
- low-volume coin subcategories under `altcoin-news`

Exit criteria:

- every top-level category has a clear purpose
- utility or franchise buckets are no longer acting like broad catch-all categories

## Phase 3. Add New Search-Led Categories

Duration: controlled rollout

Add these as new primary categories:

- `regulation`
- `companies`
- `people`
- `investigations`

Rules:

- do not bulk-move thousands of posts in one pass
- start with fresh content and a pilot backfill set
- each moved article must still have exactly one clear primary archive home

Suggested editorial rules:

- `regulation`: policy, enforcement, court, legislation, agency actions
- `companies`: exchange, protocol, issuer, public company, product, treasury, funding, M&A
- `people`: founders, executives, politicians, major public crypto voices
- `investigations`: fraud, collapse, controversy, chain forensics, accountability stories

Exit criteria:

- each new category has enough real content to justify archive indexation
- internal links and homepage modules reference the new hubs intentionally

## Phase 4. Build Narrative Hub Layer

Duration: after new primary categories are stable

Do not treat these as mass primary categories for the full archive.

Instead:

- build curated landing pages
- use editor-selected article lists
- support with internal links from related primary category pages

Examples:

- `stories/market-drama`
- `stories/company-sagas`
- `power/exchanges`
- `conflicts/regulation`
- `investigations/fraud`

Recommended implementation types:

- custom pages
- dedicated hub templates
- secondary taxonomy only if the CMS can control canonical behavior safely

Exit criteria:

- narrative hubs are additive brand assets, not new sources of archive duplication

## Phase 5. Pilot Recategorization

Duration: limited migration batch

Pilot size:

- 50 to 150 articles max

Pilot groups:

- high-traffic Bitcoin news
- regulation stories
- company stories
- investigations

What to validate:

- archive behavior
- canonical behavior
- internal links
- GSC page indexing
- GSC performance by page

Do not expand the migration until:

- redirected archive confusion is gone
- recrawl is clean enough to trust the results

## Phase 6. Expand in Waves

Only after pilot success.

Wave order:

1. new content only
2. recent 90-day content
3. top-performing evergreen content
4. older long-tail archive cleanup

Avoid:

- bulk editing the entire historical archive in one operation
- changing primary category plus permalink plus redirect logic in the same batch without testing

## Current Category Recommendations

### Keep

- `altcoin-news`
- `bitcoin-news`
- `learn-crypto`
- `press-releases`
- `sponsored-articles`

### Keep Temporarily While Migrating

- `latest-news`
- `crypto-101`
- `blockchain-events`

### Demote / Retire

- `news`
- `cmc`
- `binance`
- `top-picks`
- `pin-post`
- `mining`

### Review for Merge

- `analysis`
- `blockchain-news`
- `cryptocurrencies`
- `services`
- `crypto-exchanges`
- `crypto-wallets`

## Practical Recommendation

The first live execution should **not** be mass recategorization.

The first live execution should be:

1. archive canonical cleanup
2. archive redirect cleanup
3. template internal-link cleanup
4. recrawl
5. then create the new category layer and pilot migration

That is the cleanest way to stop CCPress from compounding the current indexation problem.
