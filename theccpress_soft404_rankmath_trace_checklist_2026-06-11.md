# TheCCPress Soft-404 Homepage Redirect Trace Checklist

Date: 2026-06-11

## Confirmed Current State

The affected trashed promo URLs are not returning a normal `404`.

They are returning:

- `301` to `https://theccpress.com/`
- response header includes `X-Redirect-By: Rank Math`

This means the homepage redirect is currently being emitted by `Rank Math` runtime.

## Already Ruled Out

- not explained by the exported `Redirection` plugin JSON file
- not explained by the Rank Math nginx batch used for duplicate article redirects
- not explained by the two homepage redirects found in the `Redirection` export

Those two homepage redirects were:

- `/?utm_source=blockspot -> /`
- `/press-releases/ -> /` and this one was disabled

Neither matches the 17 trashed promo URLs now soft-404ing to homepage.

## Affected URL Set

The current homepage-redirecting trashed URLs are:

1. `/axs-and-tia-price-charts-wobble-as-web3-ai-presale-surges/`
2. `/blockdags-0-0018-price-ends-soon-as-avax-and-bch-surges/`
3. `/blockdags-bwt-alpine-f1-deal-vs-hedera-breakout-and-solana-news/`
4. `/blockdags-presale-nears-415m-while-doge-and-myx-struggle/`
5. `/inside-blockdag-the-376m-presale-layer-1-transforming-blockchain-launches/`
6. `/next-big-crypto-coins-blockdag-vechain-chainlink-ondo/`
7. `/pepe-gains-aave-dominates-defi-blockdag-lands-f1-deal/`
8. `/blockdags-5-bonus-turns-users-into-earners/`
9. `/top-trending-crypto-blockdag-leads-pump-fun-pump-bitcoin-hyperliquid-in-2025/`
10. `/avax-price-climbs-doge-eyes-etfs-web3-ai-emerges-with-12-ai-tools/`
11. `/best-crypto-coins-to-buy-in-2025-wai-dot-link-ltc/`
12. `/best-crypto-presale-to-join-in-april-2025-qubetics-arweave-and-ethereum-latest-updates-expert-insights/`
13. `/hedera-toncoin-and-cold-wallet-the-coins-poised-for-2025-gains/`
14. `/qubetics-astra-and-injective-best-crypto-investment-opportunities-for-2025/`
15. `/qubetics-litecoin-and-arweave-top-cryptos-to-invest-in-for-short-term-in-2025/`
16. `/top-performing-crypto-why-cold-wallet-tron-stellar-pepe-are-top-of-the-line-picks-for-2025/`
17. `/web3-ai-presale-climbs-shib-stalls-ltc-eyes-105-breakout/`

## Admin Check Order

### 1. Rank Math Redirect Trace / Debug

Open any available redirect trace or debug screen inside Rank Math.

Test this example URL:

- `/axs-and-tia-price-charts-wobble-as-web3-ai-presale-surges/`

Goal:

- see whether Rank Math reports a specific matching redirect rule
- if it does, note the rule ID or name

### 2. Rank Math > Redirections

Search by source slug fragments:

- `axs-and-tia`
- `blockdags-presale-nears`
- `web3-ai-presale`
- `qubetics`

Also search for destination:

- `/`

If any rule sends one of the affected URLs to homepage, capture:

- rule ID
- source
- destination
- status

### 3. Rank Math > General Settings > Links

Review every option mentioning:

- `redirect`
- `attachment`
- `fallback`
- deleted or removed content behavior

Do not change anything yet.

### 4. Rank Math > 404 Monitor

If enabled:

- open one of the affected URLs
- check whether Rank Math suggests or auto-generates a homepage redirect

### 5. Tools > Redirection Plugin

Review:

- `Redirects`
- `Options`
- `404s`

Search the same slug fragments and search destination `/`.

This is lower probability than Rank Math, but still worth checking.

### 6. WPCode / Custom Plugin Review

If no UI rule exists, inspect custom code locations for anything that redirects deleted posts to homepage while marking the redirect as Rank Math.

Check these active custom plugins:

- `theccpress-config`
- `seo-og-fallback`
- `disable-theme-og-schema`

Check `WPCode Lite` as well.

Search for:

- `rank_math`
- `wp_redirect`
- `home_url`
- `template_redirect`
- `is_404`

## Most Likely Outcome

The most likely root cause is one of:

1. a Rank Math setting or fallback behavior for removed posts
2. a custom hook or code path that uses Rank Math redirect output

## Desired End State

These trashed promo URLs should return:

- `404`

They should not:

- `301` to homepage

## Useful Official References

- Rank Math unwanted redirects:
  - <https://rankmath.com/kb/unwanted-urls-redirecting/>
- Rank Math trace redirects:
  - <https://rankmath.com/kb/trace-url-redirects/>
- Rank Math redirections:
  - <https://rankmath.com/kb/setting-up-redirections/>
