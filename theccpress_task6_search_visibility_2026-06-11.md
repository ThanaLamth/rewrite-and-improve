# TheCCPress Task 6: Search Visibility Is Overwhelmingly Branded

Date: 2026-06-11
Verdict: `reasonable heuristic`

## Core Finding

The provided GSC export shows almost no meaningful non-brand organic search reach.

This is not strong evidence that the site has broad topic visibility yet. The export is dominated by homepage navigational demand, while the remaining impressions mostly sit on archive, hub, or legacy URL variants that generate no clicks.

## Source Files

- [`Cụm từ tìm kiếm.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Performance-on-Search-2026-06-08/C%E1%BB%A5m%20t%E1%BB%AB%20t%C3%ACm%20ki%E1%BA%BFm.csv)
- [`Trang.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Performance-on-Search-2026-06-08/Trang.csv)
- [`Quốc gia.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Performance-on-Search-2026-06-08/Qu%E1%BB%91c%20gia.csv)
- [`Thiết bị.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Performance-on-Search-2026-06-08/Thi%E1%BA%BFt%20b%E1%BB%8B.csv)
- [`Bộ lọc.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Performance-on-Search-2026-06-08/B%E1%BB%99%20l%E1%BB%8Dc.csv)

Filter context:

- Search type: `Web`
- Date range: `6 months`

## Query-Level Evidence

From the query export:

- `22` queries appear in the export
- total clicks in query export: `37`
- total impressions in query export: `304`
- branded clicks: `37 / 37 = 100%`

Branded click breakdown:

- `theccpress` = `36` clicks
- `site:theccpress.com` = `1` click

Other queries in the file produce impressions but `0` clicks, including:

- `coingeek conference press and media`
- `buy crypto press release`
- `crypto coin press release`
- `blockchain press release`
- `press release crypto`
- `crypto press release sites`

Interpretation:

- the recorded click demand is effectively navigational / brand-seeking
- the export does not show evidence of non-brand search traffic at meaningful scale

## Page-Level Evidence

From the page export:

- `16` URLs appear
- total clicks in page export: `65`
- total impressions in page export: `697`
- homepage clicks: `64 / 65 = 98.46%`

Page with non-home click:

- `/matrixport-wallets-transfer-btc-binance/` = `1` click, `10` impressions

All other visible URLs in the export have `0` clicks.

## Impression Distribution By Page Type

- homepage: `535` impressions, `64` clicks
- top-level hubs: `62` impressions, `0` clicks
- deeper hubs or post-like section URLs: `46` impressions, `0` clicks
- category variants: `44` impressions, `0` clicks
- single non-home article with clicks: `10` impressions, `1` click

## Important Nuance: Historical URL Signals Are Still Showing

Some URLs in the GSC export are legacy category-based variants that now redirect.

Live checks on 2026-06-11:

- `/category/altcoin-news/` -> `301` -> `/altcoin-news/`
- `/category/crypto-101/` -> `301` -> `/crypto-101/`
- `/category/latest-news/bitcoin-news/` -> `301` -> `/latest-news/bitcoin-news/`
- `/category/learn-crypto/blockchain-technology/` -> `301` -> `/learn-crypto/blockchain-technology/`

This means the GSC performance snapshot still contains residual visibility from older URL forms, not just the currently preferred architecture.

So the visibility problem is two-layered:

1. real lack of non-brand search demand and landing-page traction
2. residual historical indexing/query association with legacy archive variants

## Live Status of URLs Appearing in GSC Export

Currently live and `200`:

- `/`
- `/altcoin-news/`
- `/latest-news/bitcoin-news/`
- `/learn-crypto/blockchain-technology/`
- `/crypto-101/`
- `/latest-news/`
- `/news/`
- `/top-picks/crypto-exchanges/`
- `/altcoin-news/ethereum/`
- `/press-releases/`
- `/cmc/`

Currently redirecting:

- `/category/altcoin-news/`
- `/category/crypto-101/`
- `/category/latest-news/bitcoin-news/`
- `/category/learn-crypto/blockchain-technology/`

## What This Actually Means

This export does not support the idea that TheCCPress has broad topic coverage in Google Search yet.

Instead, it suggests:

- the brand/homepage is doing nearly all the visible work
- hub and archive URLs are being surfaced for some intents, but not converting into clicks
- some of the indexed/query-associated URLs are still historical or transitional variants

## Recommended Next Moves

### 1. Finish stabilizing preferred URL signals

The redirects are now in place, but GSC still reflects old variants.

Need:

- fresh crawl
- refreshed internal linking
- resubmitted clean sitemap set
- time for Google to consolidate signals away from old `/category/` variants

### 2. Pick a smaller durable hub set

Instead of spreading thin signals across many sections, support a smaller set of stable indexable hubs.

Candidate durable hubs already visible in the export:

- `/latest-news/`
- `/altcoin-news/`
- `/crypto-101/`
- `/learn-crypto/blockchain-technology/`
- `/top-picks/crypto-exchanges/`
- `/press-releases/`

### 3. Build non-brand evergreen landing pages

The biggest gap is not just technical. It is the absence of clear non-brand landing pages earning query clicks.

The site needs evergreen pages with stronger intent alignment around:

- beginner crypto concepts
- exchange comparisons
- wallet/compliance/regulation explainers
- structured topical hubs linked from sitewide navigation and relevant articles

### 4. Re-check after the next crawl/indexing cycle

The right test after the redirect cleanup is:

- whether old category variants disappear from performance exports
- whether clean hub URLs gain impressions and clicks
- whether homepage click concentration begins to weaken

## Bottom Line

The current GSC export is overwhelmingly branded.

Numerically:

- `100%` of query-export clicks are branded
- `98.46%` of page-export clicks go to the homepage

That is the clearest sign that current search visibility is not yet diversified across durable non-brand landing pages.
