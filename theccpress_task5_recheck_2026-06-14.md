# TheCCPress Task 5 Recheck

Date: 2026-06-14
Scope: re-evaluate crawl instability signals after redirect cleanup, promo prune, and soft-404 cleanup

## Current Read

Task 5 is still real, but it is now clearer that it has `2` different layers:

1. real URL waste and stale crawl targets
2. a smaller but still plausible crawler-access instability layer

## Local Crawl Counts

From local crawl exports:

- crawl `2nd`: `0 = 1844`, `403 = 840`, `404 = 806`, `200 = 19035`
- crawl `3rd`: `0 = 737`, `403 = 872`, `404 = 396`, `200 = 8465`

The raw counts improved materially on `0` and `404`, but not on `403`.

## Important Refinement From The 3rd Crawl

Not all `0` and `403` rows are internal page-access problems on `theccpress.com`.

From `/home/qcweb/ccpress 3rd/response_codes_all.csv`:

- internal `0` rows: `396`
- external `0` rows: `341`
- internal `403` rows: `717`
- external `403` rows: `155`

This matters because a meaningful share of the noise comes from:

- external profile URLs
- external article links
- external embeds
- internal image assets

So the raw crawl totals overstate how much of the problem is a live HTML-page block on the main site.

## Live Recheck On 2026-06-14

Sample internal URLs that had `0` or `403` in the local crawl were re-tested using:

- browser UA
- Googlebot-like UA
- Screaming Frog UA
- both `GET` and `HEAD`

### URLs that now return stable `200`

- `/trading-bots-the-ultimate-guide/`
- `/ray-dalio-cbdcs-privacy-risks/`
- `/south-korea-police-probe-polymarket-illegal-gambling/`
- `/author/nathan-sinclair/?section=review`
- `/wp-content/uploads/2026/02/vitalik-buterin-blockchain-scene-file-350x250.jpeg`

These returned the same response for:

- browser `GET` and `HEAD`
- Googlebot-like `GET` and `HEAD`
- Screaming Frog `GET` and `HEAD`

### URLs that now return real `404`

- `/u-s-senators-push-regulators-to-revisit-bitcoins-1250-risk-weight-rule/`
- `/spot-bitcoin-etfs-record-2-4b-may-outflows/`
- `/brazilian-public-company-oranjebtc-buys-41-more-bitcoin-holdings-reach-3803-btc/`
- `/bitcoin-etfs-bought-3350-btc-worth-240m-on-april-10/`
- `/binance-pre-ipo-market-entry-reported-on-telegram/`

These also returned the same result across:

- browser
- Googlebot-like
- Screaming Frog
- `GET`
- `HEAD`

## What This Means Now

The current evidence does `not` support a simple explanation like:

- Googlebot is blocked sitewide
- Screaming Frog is blocked sitewide
- `HEAD` requests are blocked while `GET` passes

Instead, the remaining likely interpretations are:

1. some portion of the old `0/403` rows were transient crawler/session failures
2. some portion were stale targets that now correctly return `404`
3. some portion were non-HTML assets or external URLs that inflated the crawl-noise picture

## What I Can Do Versus What Needs Dev

### I can do

- keep separating true internal HTML failures from crawl noise
- build narrower recheck batches from the local crawl files
- identify whether the remaining bad rows are mostly assets, archives, query-parameter URLs, or dead posts
- keep refining the dev handoff with concrete URL samples

### Dev access is still required for

- Cloudflare Security Events
- WAF and rate-limit review
- LiteSpeed / origin logs
- any evidence tied to verified Googlebot sessions
- request-failure analysis by IP, ASN, or edge/origin status

## Practical Conclusion

Task 5 is `doable` on the audit side and still worth pursuing.

But the highest-value remaining move is not generic re-crawling alone.

It is:

1. isolate the remaining `internal same-host 0/403` rows by URL type
2. remove obvious crawl-noise classes
3. hand the narrowed residual set to dev for edge/origin log inspection
