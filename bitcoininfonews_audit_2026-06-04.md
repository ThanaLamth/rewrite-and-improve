# BitcoinInfoNews SEO Audit

Date: 2026-06-04
Domain: `https://bitcoininfonews.com/`
Verdict: `at risk`

## Scope

This audit is based on the local crawl and GSC export bundle in `/home/qcweb/bitcoininfonews/`:

- `internal_all.csv`
- `internal_html.csv`
- `response_codes_all.csv`
- `directives_all.csv`
- `canonicals_all.csv`
- `all_inlinks.csv`
- `sitemaps_all.csv`
- `search_console_all.csv`
- `GSC/*`

Official Google guidance referenced:

- Search Essentials
- Helpful, reliable, people-first content
- AI features and your website
- Block indexing
- Consolidate duplicate URLs
- Large site crawl budget guidance
- Build and submit a sitemap
- Article structured data
- Spam policies

## Executive Summary

The site is technically crawlable and the host is stable, but the main risk is not server health. The site has a large amount of duplicate and low-value URL inventory, heavily polluted sitemap-derived URL sets, major internal link waste, and a content mix that leans hard into promotional search-first publishing.

The strongest concern is the combination of:

1. too many non-indexable or duplicate URLs in sitemap-derived inventory
2. too many internal links hitting redirects or dead URLs
3. too many indexable promotional pages and duplicated `-2`, `-3`, `-4` style URLs
4. a clear mismatch between the site's editorial standards page and the live content footprint

## High-Risk Findings

### 1. Sitemap-derived URL set is polluted

Status: `officially supported`

From `sitemaps_all.csv`, out of 18,276 URLs:

- 13,882 are indexable
- 4,394 are non-indexable
- 3,932 are `noindex`
- 415 are `404`
- 47 are `301`

This means roughly 24.04% of sitemap-derived URLs are not eligible target URLs for search.

Why this matters:

- Google sitemap guidance expects sitemaps to contain the URLs you actually want indexed.
- Mixed signals reduce confidence in preferred canonical targets.
- This wastes crawl attention and increases indexation noise.

Examples:

- tag URLs included but `noindex`
- search result URLs included but `noindex`
- article URLs included but `404`
- redirected archive URLs included

Primary fix:

- regenerate sitemap logic so that only `200`, canonical, indexable URLs are included
- remove all `noindex`, `404`, and `301` URLs from sitemap outputs

### 2. Numbered duplicate posts are indexable

Status: `officially supported`

The crawl found 1,321 indexable suffixed URLs like:

- `.../something-2/`
- `.../something-3/`
- `.../something-4/`

There are 1,489 duplicate groups in the sitemap-derived set.

Examples:

- `https://bitcoininfonews.com/prediction-markets-bitcoin-below-60000-june-2/`
- `https://bitcoininfonews.com/vitalik-proposes-defi-design-to-reduce-liquidations-2/`
- multiple `republic-europe-kraken-*` clusters with many numbered variants

Why this matters:

- Google recommends consolidating duplicates and signaling one preferred URL.
- Indexable duplicates split relevance, waste crawl budget, and lower trust in content quality.

Primary fix:

- identify the publishing workflow creating numbered copies
- choose one preferred URL per cluster
- `301` the replaced duplicates where appropriate
- temporarily `noindex` duplicates if staged cleanup is required
- remove duplicate losers from sitemaps

### 3. Internal linking waste is severe

Status: `officially supported`

From `all_inlinks.csv`:

- 4,079,800 total inlinks processed
- 3,429,065 internal inlinks
- 2,520,488 internal inlinks to `200`
- 907,832 internal inlinks to `301`
- 745 internal inlinks to `404`

Of the 301 links:

- 907,800 point to month archive URLs such as `/2025/04/`

Examples:

- `/2024/12/` -> `301` to homepage
- `/2026/04/` -> `301` to homepage

Why this matters:

- Google crawl budget guidance explicitly warns that duplicate and unimportant URLs can drain crawl resources.
- Internal links should point directly to final canonical URLs.

Primary fix:

- remove the template logic creating month archive internal links
- update internal links to point directly to final destination URLs
- clean malformed internal targets like `/cdn-cgi/l/email-protection`, `/IMAGE_URL`, and `/source`

### 4. Too many deep paginated archives are indexable

Status: `reasonable heuristic`

Indexable paginated archive URLs found:

- 1,446 indexable paginated archives
- 1,473 indexable archive-like pages in total

Examples:

- `/crypto-news/page/223/`
- `/cmc/page/104/`
- `/sponsored-articles/page/72/`

Why this matters:

- Google does not ban indexed pagination, but this is excessive relative to the site's actual search traction.
- Deep archive pages with repetitive titles and generic summaries usually create index bloat on sites like this.

Primary fix:

- keep primary hub pages indexable
- test `noindex,follow` or pruning for deep paginated archives
- start with `cmc`, `sponsored-articles`, and very deep category pagination

### 5. Promotional inventory is too large

Status: `policy-risk / at risk`

The crawl found 875 indexable posts matching strongly promotional patterns in titles:

- `presale`: 760
- `meme coin`: 379
- ROI-style phrases: 333
- `buy now`: 130
- `price prediction`: 108
- `best crypto to buy`: 62

Examples:

- `2900% ROI? 2X Offer? BTFD Coin Is the Best Crypto to Buy NOW...`
- multiple BlockDAG, Qubetics, meme coin, presale, and ROI pages

Why this matters:

- Google's helpful content guidance focuses on people-first value, expertise, and original contribution.
- In a finance-adjacent niche, aggressively promotional content at scale is a trust risk.

Primary fix:

- freeze net-new promo content until cleanup is complete
- prune or consolidate low-value promo clusters
- require stronger sourcing and clear original value before publishing similar content

### 6. Editorial standards and live inventory conflict

Status: `policy-risk / at risk`

The public page `editorial-standards-fact-checking-policy/` says the site is Bitcoin-first, disciplined, and not focused on broad altcoin or low-value duplication. The live inventory does not match that claim.

Observed live footprint includes:

- large altcoin and meme coin coverage
- many presale and sponsored pages
- many duplicated numbered articles
- large indexable archive footprints for `cmc` and `sponsored-articles`

Why this matters:

- this is a trust and consistency problem
- weak alignment between stated editorial scope and actual output can reduce reader and search trust

Primary fix:

- either align the site to the Bitcoin-first policy in practice
- or rewrite the editorial policy so it accurately reflects the content and business model

### 7. Sponsored content is disclosed, but still risky at scale

Status: `unclear / needs testing`

Sampled sponsored pages do include visible disclaimers. Example:

- the BTFD article includes a disclaimer saying the advertorial is not part of editorial content

This is better than hiding the commercial nature of the page. However:

- sponsored pages are still indexable
- the sponsored section is large
- sponsored and editorial content remain tightly mixed inside the same site architecture

Primary fix:

- keep clear disclosure
- consider `noindex` for sponsored archive pages at minimum
- audit sponsored outbound links and confirm correct relationship attributes where needed

### 8. Some article URLs are accidentally noindexed

Status: `officially supported`

At least two normal article-like URLs return `200` with `follow, noindex`:

- `https://bitcoininfonews.com/pippin-pippin-shows-increasing-on-chain-participation-as-solana-network-engagement-rises/`
- `https://bitcoininfonews.com/united-stables-u-demonstrates-elastic-liquidity-as-redemptions-scale/`

Why this matters:

- accidentally noindexed articles cannot rank
- this is especially bad if those pages are meant to be part of core editorial inventory

Primary fix:

- audit all standalone article URLs with `noindex`
- keep only intentionally excluded ones as `noindex`

### 9. Search traction is extremely low relative to inventory

Status: `reasonable heuristic`

From the GSC performance export covering 16 months:

- 830 total clicks
- 2,672 total impressions
- only 26 pages show clicks in the exported page report
- query clicks are heavily branded or navigational

Examples:

- `bitcoin network transactions hit 11-month low bitcoininfonews`
- `pump.fun token launch rumors officially quelled bitcoininfonews`
- `bitcoininfonews.com`

Why this matters:

- the site is publishing far more indexable inventory than it is earning trust or demand for
- this argues for pruning and focus, not more volume

Primary fix:

- reduce the indexed footprint
- focus on a smaller, higher-trust, source-driven core set

## Supporting Data

### HTML crawl summary

From `internal_html.csv`:

- 18,276 HTML URLs
- 17,814 return `200`
- 415 return `404`
- 47 return `301`
- 13,882 are indexable
- 4,394 are non-indexable

Non-indexable breakdown:

- tag `noindex`: 2,322
- author pagination `noindex`: 1,236
- search `noindex`: 360
- author pages `noindex`: 12

### Archive and duplicate footprint

- 1,446 indexable paginated archives
- 1,473 indexable archive-like pages
- 1,321 indexable suffixed duplicate URLs

### Internal link debt

- 907,832 internal links to redirects
- 907,800 internal links to month archive redirects
- 745 internal links to 404 targets

### 404 inventory

- 415 internal site URLs return `404`
- top repeated broken target: `/cdn-cgi/l/email-protection`
- additional broken article URLs still receive internal links

## Strong Positives

- core article pages are generally indexable and self-canonical
- host health looks stable in crawl stats
- article structured data is implemented
- transparency pages exist:
  - `/about/`
  - `/contact-us/`
  - `/privacy-policy/`
  - `/terms-and-conditions/`
  - `/content-disclaimer/`
  - `/editorial-standards-fact-checking-policy/`

## Priority Order

1. clean sitemap generation
2. consolidate numbered duplicates
3. remove internal links to redirected month archives
4. fix internal links to 404 targets
5. review accidental `noindex` article URLs
6. reduce indexable deep archive pagination
7. prune and consolidate promotional inventory
8. align live inventory with editorial policy

## Next Step

The next deliverable should be an action sheet with:

- exact URLs to `301`
- exact URLs to `noindex`
- exact URLs to keep
- batch order by impact and implementation clarity
