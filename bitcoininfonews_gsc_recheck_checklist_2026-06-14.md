# BitcoinInfoNews GSC Recheck Checklist - 2026-06-14

## Recheck window
- Recheck after 7 days: 2026-06-21
- Optional early spot check after 3 days: 2026-06-17

## What to check in GSC
- URL Inspection for a sample of the 104 URLs noindexed on 2026-06-12
- Coverage / Pages report to confirm excluded by `noindex`
- Performance report to confirm impressions for low-value noindexed URLs fade down
- Page indexing for `https://bitcoininfonews.com/millionaire/`
- Page indexing for `https://bitcoininfonews.com/blockchain-events/`

## Expected outcomes
- The 104 low-value URLs should move out of indexed state
- `millionaire/` and `blockchain-events/` should remain crawlable but not indexed
- No deleted promo URLs should redirect to homepage

## If something is still wrong
- If a noindexed URL is still indexed after recrawl, inspect live source for robots meta and request reindexing only if needed
- If `millionaire/` or `blockchain-events/` start getting indexed, convert them from `200 + noindex` to a harder final state later
- If old promo URLs start redirecting again, re-check attachment or fallback redirect behavior first
