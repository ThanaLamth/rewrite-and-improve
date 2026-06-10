# TheCCPress Dev Handoff: Task 5 Crawl Efficiency and Crawl Stability

Date: 2026-06-10
Domain: `https://theccpress.com/`

## Objective

Investigate and fix crawl instability and crawler inefficiency after the main redirect and broken-link cleanup.

This is not only a URL-waste problem. Historical evidence suggests an intermittent access/stability problem affecting crawler sessions.

## What Has Already Been Fixed

- High-priority internal broken links were cleaned up.
- Priority redirect batches were imported and verified live.
- Broken-link cleanup covered the highest-impact 404 targets first.

Related local files:

- [`theccpress_404_priority_assessment_2026-06-09.csv`](/home/qcweb/rewrite-and-improve/theccpress_404_priority_assessment_2026-06-09.csv)
- [`theccpress_redirection_pending_bulk_2026-06-09.csv`](/home/qcweb/rewrite-and-improve/theccpress_redirection_pending_bulk_2026-06-09.csv)
- [`theccpress_redirection_remaining_batch_2026-06-09.csv`](/home/qcweb/rewrite-and-improve/theccpress_redirection_remaining_batch_2026-06-09.csv)

## Evidence

### Google Search Console Crawl Stats

Source files:

- [`Bảng phản hồi.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Crawl-stats-2026-06-08/B%E1%BA%A3ng%20ph%E1%BA%A3n%20h%E1%BB%93i.csv)
- [`Bảng loại tệp.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Crawl-stats-2026-06-08/B%E1%BA%A3ng%20lo%E1%BA%A1i%20t%E1%BB%87p.csv)
- [`Bảng mục đích.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Crawl-stats-2026-06-08/B%E1%BA%A3ng%20m%E1%BB%A5c%20%C4%91%C3%ADch.csv)
- [`Bảng thông tin máy chủ.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Crawl-stats-2026-06-08/B%E1%BA%A3ng%20th%C3%B4ng%20tin%20m%C3%A1y%20ch%E1%BB%A7.csv)
- [`Biểu đồ tóm tắt thống kê thu thập dữ liệu.csv`](/home/qcweb/GSC%20CCpress/theccpress.com-Crawl-stats-2026-06-08/Bi%E1%BB%83u%20%C4%91%E1%BB%93%20t%C3%B3m%20t%E1%BA%AFt%20th%E1%BB%91ng%20k%C3%AA%20thu%20th%E1%BA%ADp%20d%E1%BB%AF%20li%E1%BB%87u.csv)

Key findings:

- `404` responses = `51.59%` of crawl requests
- `200` responses = `41.34%`
- `other 4XX` = `2.34%`
- `301` = `0.68%`
- `unknown failed requests` by file type = `54.28%`
- crawl purpose = `97% refresh`, `3% discovery`
- server status for `theccpress.com` = `Có vấn đề trước đây`
- GSC recorded `31,714` crawl requests on `theccpress.com`

### Local Crawl Data

Source files:

- [`/home/qcweb/ccpress 2nd/response_codes_all.csv`](/home/qcweb/ccpress%202nd/response_codes_all.csv)
- [`/home/qcweb/ccpress 3rd/response_codes_all.csv`](/home/qcweb/ccpress%203rd/response_codes_all.csv)

Counts:

- Crawl `2nd`: `status 0 = 1,844`, `403 = 840`, `404 = 806`
- Crawl `3rd`: `status 0 = 737`, `403 = 872`, `404 = 396`

### Stability Signal

This is the strongest signal that this is not just a bad-URL problem:

- Top `20` URLs with `status 0` in crawl `2nd` were live-rechecked on `2026-06-10`
- Result: `20/20` now return `200`

Examples:

- `/advertise/`
- `/about-us/`
- `/author/noah-carter/`
- `/author/lorena/`
- `/sec-clears-key-regulatory-hurdle-for-grayscales-hyperliquid-staking-etf/`

Also:

- Top `15` URLs with `403` in crawl `3rd` were live-rechecked on `2026-06-10`
- Result: `14/15` now return `200`
- Only notable failure in that spot check was `/sponsored-articles/`, which currently resolves into a bad archive path ending in `404`

### Public Behavior Tests Already Performed

Tested with:

- normal `curl` UA
- `Screaming Frog SEO Spider/22.0` UA
- Googlebot-like UA
- both `HEAD` and `GET`

Sample URLs tested:

- `/sbi-vc-trade-launches-solana-trading-custody-and-asset-management-services/`
- `/top-picks/crypto-exchanges/`
- `/tag/ethereum/`
- `/binance-shut-down-nft-support-exchange-move-service-wallet/`

Result:

- all tested combinations returned `200` at time of recheck
- no current fixed block by UA or HTTP method was reproduced publicly

## Working Interpretation

Two issues likely overlap:

1. Real crawl waste from historic 404s, redirecting URLs, and low-value paths
2. Intermittent crawler-access instability at edge or origin level

The instability may be caused by one or more of:

- Cloudflare Security / WAF / Bot Fight / Rate Limiting rules
- LiteSpeed or origin throttling
- intermittent origin performance or worker saturation
- edge challenge or mitigation behavior not visible in simple public spot checks

## What Dev Needs To Check

### 1. Cloudflare

Check:

- Security Events
- WAF managed rules
- custom firewall rules
- Bot Fight / Super Bot Fight
- rate limiting rules
- challenge or JS challenge actions
- cache rules that may vary by bot or path class

Focus filters:

- Googlebot verified traffic
- requests to article URLs, `/tag/`, author pages, archive pages, and image URLs
- windows where crawl volume dropped hard from about `~1000/day` to about `~150-300/day`

Need from dev:

- whether Googlebot, generic bots, or Screaming Frog-like traffic were challenged, blocked, rate-limited, or served atypical responses

### 2. Origin / LiteSpeed / WAF

Check:

- LiteSpeed anti-DDoS or anti-bot features
- ModSecurity / OWASP events
- origin `403`, `429`, `5xx`, connection reset, timeout, and early close events
- whether `HEAD` requests are treated differently than `GET`
- whether image paths or tag archives are disproportionately denied

Need from dev:

- confirm if origin saw crawler requests that never completed cleanly
- confirm if origin emitted `403` while public retests now show `200`

### 3. Log Comparison

Compare:

- verified Googlebot traffic
- standard browser traffic
- Screaming Frog traffic if available

Look for:

- status mismatches by UA
- repeated failed requests to otherwise healthy URLs
- IP reputation or ASN-based blocking
- spikes in `403`, `499`, `524`, `520`, `521`, `522`, `523`, `524`

### 4. Verify Googlebot Properly Before Any Allowlist

If allowlisting is considered, do it only after verified reverse DNS / forward DNS validation of Googlebot.

Official references:

- Crawl budget guidance: `https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget`
- Verify Googlebot: `https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot`
- Crawl Stats report help: `https://support.google.com/webmasters/answer/9679690`

## Priority Questions For Dev To Answer

1. Did Cloudflare or origin security rules challenge or block crawler sessions during March to June 2026?
2. Are there logs showing intermittent `403` or failed connections for URLs that are currently `200`?
3. Are `HEAD` requests, image requests, or tag/archive requests handled differently from normal article `GET` requests?
4. Is there any origin saturation, timeout, or upstream issue that explains the large `status 0` population in Screaming Frog while live rechecks succeed?

## Expected Outcome

We need a clear answer to this:

- Is Google mostly wasting crawl on bad URLs only?
- Or is Google also hitting intermittent bot/access instability on otherwise valid URLs?

Current evidence supports: both are happening, with the second issue still unresolved.
