# Google Trends Watch Checkpoint

Date: 2026-05-06

This checkpoint snapshots the current Google Trends watcher that was built under the local Codex skill workspace and copied here for versioned backup.

## Included

- `scripts/google_trends_finance_watch.py`
- `scripts/run_google_trends_finance_watch.sh`
- `references/automation.md`

## What This Watcher Does

- Fetches Google Trends RSS for multiple GEOs.
- Filters items to crypto, finance, markets, business, and policy topics that may affect crypto prices.
- Sends matched items to Telegram topic thread `7`.
- Suppresses duplicate alerts by persisting seen item IDs locally.

## Current GEO Set

`AE,SG,TR,AR,TH,BR,VN,US,SA,MY,HK,ID,KR,ZA,CH,PH,VE,UA,CA,SI,MX,AU,CL,IE,NO,BE,CY,DE,IN`

Notes:

- `LU` was excluded from the default set because the Google Trends RSS endpoint returned `HTTP 400` for that GEO during testing.

## Telegram Message Format

- No `New matches:` count line.
- No `Source` footer.
- Header shows the GEO set.
- Each item shows `[GEO] Country: keyword (traffic)` plus short source links.

## Current Cron Job

```cron
0 */2 * * * /home/googleupdate/.codex/skills/google-search-seo-watch/scripts/run_google_trends_finance_watch.sh >> /home/googleupdate/.codex/memories/google-trends-finance.log 2>&1
```

## Secrets

The live env file with Telegram credentials remains outside this repo:

- `/home/googleupdate/.codex/memories/google-search-seo-watch.env`

It was intentionally not committed.
