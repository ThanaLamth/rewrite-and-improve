# TheCCPress Task 7: Duplicate Article Clusters and Suffixed Slugs

Date: 2026-06-11
Verdict: `reasonable heuristic`

## Core Finding

The duplicate-content risk here is not about exact HTML alone.

The stronger issue is repeated story publication around the same topic, often with:

- identical page titles across multiple indexable URLs
- multiple near-identical slug variants
- suffix-heavy slugs like `-2`, `-3`, `-4`, `-5`

That pattern can split relevance, crawl attention, and link equity across competing URLs.

## Source

- [`/home/qcweb/ccpress 2nd/internal_all.csv`](/home/qcweb/ccpress%202nd/internal_all.csv)

## Primary Numbers

From the `ccpress 2nd` crawl:

- `42` duplicate title clusters exist among indexable `200` HTML pages
- those clusters cover `91` indexable URLs
- `95` indexable URLs have slug suffixes like `-2`, `-3`, `-4`, or `-5`

Important note:

- `ccpress 3rd` only shows `3` duplicate clusters and `6` suffix URLs
- that does **not** mean the problem is fixed
- it is more likely because `ccpress 3rd` is a narrower follow-up crawl, not a full replacement scope for this analysis

## Largest Duplicate Clusters

### 1. Arizona Governor Vetoes Bitcoin Reserve Bill

Cluster size: `6`

URLs:

- `https://theccpress.com/arizona-governor-vetoes-bitcoin-bill/`
- `https://theccpress.com/arizona-governor-bitcoin-reserve-veto/`
- `https://theccpress.com/arizona-governor-vetoes-bitcoin-reserve-bill-2/`
- `https://theccpress.com/arizona-bitcoin-reserve-bill-veto/`
- `https://theccpress.com/arizona-governor-vetoes-bitcoin-bill-2/`
- `https://theccpress.com/arizona-governor-vetoes-bitcoin-bill-3/`

Recommended keeper:

- `https://theccpress.com/arizona-bitcoin-reserve-bill-veto/`

### 2. REX Shares Files for Ethereum and Solana Staking ETFs

Cluster size: `3`

URLs:

- `https://theccpress.com/rex-ethereum-solana-staking-etfs-announcement/`
- `https://theccpress.com/rex-shares-ethereum-solana-staking-etfs/`
- `https://theccpress.com/rex-ethereum-solana-staking-etfs/`

Recommended keeper:

- `https://theccpress.com/rex-ethereum-solana-staking-etfs/`

### 3. REX Shares Files for Ethereum, Solana Staking ETFs

Cluster size: `3`

URLs:

- `https://theccpress.com/ethereum-solana-staking-etf-filing/`
- `https://theccpress.com/rex-shares-ethereum-solana-etfs/`
- `https://theccpress.com/rex-shares-ethereum-solana-staking-etfs-2/`

Recommended keeper:

- `https://theccpress.com/rex-shares-ethereum-solana-etfs/`

### 4. SEC Approves In-Kind Redemptions for Bitcoin, Ethereum ETFs

Cluster size: `3`

URLs:

- `https://theccpress.com/sec-approves-in-kind-redemptions-bitcoin-ethereum-etfs/`
- `https://theccpress.com/sec-approves-bitcoin-ethereum-etf-redemptions/`
- `https://theccpress.com/sec-approves-in-kind-redemptions-etfs/`

Recommended keeper:

- `https://theccpress.com/sec-approves-in-kind-redemptions-etfs/`

## Notable Two-URL Clusters

Examples:

- Ant Group / Circle / USDC
- Argentina crypto adoption
- Avalanche DeFi TVL
- Binance KYC re-verification India
- Bitcoin ATH in Argentina
- Bitwise CEO Wall Street crypto adoption
- BlackRock ETF outflow
- Brown University Bitcoin ETF
- CME Group Solana/XRP futures launch

These are smaller than the big clusters, but still worth cleaning because they are indexable duplicates.

## Suffix-Slug Pattern

The `95` suffix-heavy URLs suggest a repeatable publishing workflow problem, not random one-off mistakes.

Examples:

- `...-2`
- `...-3`
- `...-4`
- `...-5`

High-risk examples include:

- `blockdag-joins-global-exchanges-...-2`
- `the-next-crypto-to-explode-...-2`
- multiple `truth-social-bitcoin-etf` variants
- multiple `bitcoin-surpasses-amazon-market-cap` variants
- multiple `texas-bitcoin-reserve-bill` variants
- multiple `whale-buys-1b-pump-tokens` variants

## Why This Matters

Even when body copy is not identical, this pattern can still damage search performance because:

- Google must choose among too many URLs for the same story intent
- internal links and crawl attention are split
- title duplication weakens topic differentiation
- suffix-based republishing often creates low-trust editorial signals

## Recommended Fix Framework

### 1. Story-Level Clustering

For each duplicate topic:

- keep one strongest URL
- decide whether weaker URLs should be:
  - `301` redirected
  - `noindex`
  - merged into the keeper
  - deleted if they add no value

### 2. Keeper Selection Rule

Choose the keeper using this order:

1. strongest internal inlinks
2. cleanest non-suffix slug
3. strongest title phrasing
4. best chance of external mentions already pointing to it

### 3. Default Rule for Suffix URLs

If a suffix URL is just another version of the same story:

- do not leave it indexable
- redirect it to the keeper unless there is a very strong reason to preserve it separately

### 4. Workflow Review

Editorial / CMS workflow needs review because the suffix pattern looks systemic.

Questions to answer:

1. are editors re-posting the same story instead of updating the original?
2. are drafts being republished under new slugs?
3. is an import or syndication process creating duplicates automatically?
4. are multiple writers publishing near-identical takes on the same news event without consolidation?

## Priority Cleanup Order

### Tier 1

Clean first:

1. Arizona Governor veto cluster
2. both REX staking ETF clusters
3. SEC in-kind ETF redemption cluster

### Tier 2

Then clean:

1. BlockDAG duplicated commercial story pairs
2. Bitcoin/Amazon market cap duplicates
3. Truth Social Bitcoin ETF duplicates
4. Texas Bitcoin reserve bill duplicates

### Tier 3

Then review the broader suffix-heavy publication set from 2025-2026 and apply batch decisions.

## Practical Next Step

Build a duplicate cluster sheet with:

- title cluster
- all URLs in cluster
- keeper URL
- action for every weaker URL

That is the fastest way to turn this from an audit finding into execution.
