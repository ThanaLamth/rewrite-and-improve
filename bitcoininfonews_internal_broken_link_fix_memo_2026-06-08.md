# BitcoinInfoNews internal broken link fix memo

- Broken targets in input sheet: 415
- Broken-link occurrences in source pages: 745
- Unique source pages affected: 301
- Replace target actions: 346
- Unlink actions: 365
- Cloudflare email-protection rows skipped from content edits: 34

## Execution rule

- `replace_link_target`: switch broken href to the closest live article URL.
- `unlink_keep_anchor_text`: remove the hyperlink but keep its visible text.
- `skip_cloudflare_email_protection`: email-protection links are rendered at edge level and were not found as broken hrefs in WP raw content.

## Live apply result

- Applied live edits through WordPress REST to 271 actionable source pages.
- Verified editable source pages with REST raw-content readback: 268/268 returned `remaining_old_href_hits = 0`.
- Remaining 3 actionable source URLs were not editable because the source URLs themselves are now 404 and do not resolve to a live post ID:
  - `https://bitcoininfonews.com/xrp-commodity-status-etf-momentum-price-target-5-5/`
  - `https://www.bitcoininfonews.com/t-rowe-price-updates-crypto-etf-as-tradfi-fomo-drives-inflow-surge/`
  - `https://www.bitcoininfonews.com/xrp-beats-bitcoin-and-ethereum-in-south-korea-as-volume-spikes-115/`
- 30 additional source pages were `skip_cloudflare_email_protection` only, so no WordPress content edit was needed there.
