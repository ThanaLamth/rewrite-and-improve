# Automation

## Goal

Run a small watcher outside Codex so you get notified when official Google Search pages change.

The recommended helper is:

- [scripts/google_update_watch.py](../scripts/google_update_watch.py)
- [scripts/roundtable_google_news_watch.py](../scripts/roundtable_google_news_watch.py)

## Telegram Setup

Provide either flags or environment variables:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `TELEGRAM_OFFICIAL_THREAD_ID` for official Google alerts
- `TELEGRAM_ROUNDTABLE_THREAD_ID` for Search Engine Roundtable follow-up
- `TELEGRAM_MESSAGE_THREAD_ID` only as a generic fallback

Example:

```bash
export TELEGRAM_BOT_TOKEN="123456:token"
export TELEGRAM_CHAT_ID="-1003747295451"
export TELEGRAM_OFFICIAL_THREAD_ID="2"
export TELEGRAM_ROUNDTABLE_THREAD_ID="3"
python3 ~/.codex/skills/google-search-seo-watch/scripts/google_update_watch.py \
  --state ~/.codex/memories/google-search-seo-watch-state.json \
  --send-telegram
```

## Values Extracted From Your Telegram Payload

From the payload you shared:

- `chat_id`: `-1003747295451`
- `message_thread_id=2`: `Google Core Update`
- `message_thread_id=3`: `Google Update Discussion from Roundtable`
- `message_thread_id=7`: `Trending Keyword Daily`

Current mapping:

- official Google changes from Search Central or Search Status Dashboard: thread `2`
- Search Engine Roundtable follow-up and commentary: thread `3`
- `Trending Keyword Daily` thread `7`: use for Google Trends or keyword alerts

## Roundtable Google News

Use the dedicated Roundtable watcher when you want topic `3` to receive Google-related news directly from Search Engine Roundtable, even when there is no new official Google alert.

Command:

```bash
python3 ~/.codex/skills/google-search-seo-watch/scripts/roundtable_google_news_watch.py \
  --state ~/.codex/memories/roundtable-google-news-state.json \
  --send-telegram
```

Wrapper:

```bash
/home/googleupdate/.codex/skills/google-search-seo-watch/scripts/run_roundtable_google_news_watch.sh
```

Behavior:

- reads the Roundtable feed
- keeps only Google-related posts
- skips the first run by creating a baseline state
- sends only unseen items after that
- posts into `TELEGRAM_ROUNDTABLE_THREAD_ID`, currently thread `3`

## Google Trends Finance-Related RSS

Use the dedicated Google Trends watcher when you want topic `7` to receive US `Trending now` RSS items that look finance-related.

Command:

```bash
python3 ~/.codex/skills/google-search-seo-watch/scripts/google_trends_finance_watch.py \
  --state ~/.codex/memories/google-trends-finance-state.json \
  --send-telegram
```

Wrapper:

```bash
/home/googleupdate/.codex/skills/google-search-seo-watch/scripts/run_google_trends_finance_watch.sh
```

Behavior:

- reads `https://trends.google.com/trending/rss?geo=...` for each GEO in `GOOGLE_TRENDS_GEOS`
- if `GOOGLE_TRENDS_GEOS` is unset, falls back to `US`
- keeps only filtered crypto / markets / finance / policy items
- skips the first run by creating a baseline state unless `--send-empty-test` is used
- posts into `TELEGRAM_TRENDS_THREAD_ID`, default thread `7`

## Cron Example

Run every 30 minutes:

```bash
TELEGRAM_BOT_TOKEN="123456:token" TELEGRAM_CHAT_ID="-1003747295451" TELEGRAM_OFFICIAL_THREAD_ID="2" TELEGRAM_ROUNDTABLE_THREAD_ID="3" */30 * * * * /usr/bin/python3 /home/googleupdate/.codex/skills/google-search-seo-watch/scripts/google_update_watch.py --state /home/googleupdate/.codex/memories/google-search-seo-watch-state.json --send-telegram >> /home/googleupdate/.codex/memories/google-search-seo-watch.log 2>&1
```

Roundtable daily example:

```bash
0 9 * * * /home/googleupdate/.codex/skills/google-search-seo-watch/scripts/run_roundtable_google_news_watch.sh >> /home/googleupdate/.codex/memories/roundtable-google-news.log 2>&1
```

## Operating Notes

- The first run creates the baseline state and should not be treated as a change event.
- A feed or incident fingerprint change means "inspect this source now", not "Google definitely changed ranking behavior".
- When official sources change, the script sends one official alert to thread `2` and one Roundtable follow-up message to thread `3` if it finds new relevant RSS items.
- After an alert:
  1. read the official page that changed
  2. summarize the exact official delta
  3. check Search Engine Roundtable for commentary
  4. decide whether the user's site or article needs action

## Default Watch Targets

The helper script watches these by default:

- documentation updates RSS
- Search updates page
- core updates guidance page
- helpful content guidance page
- Search Essentials
- spam policies
- Search Status Dashboard Atom feed
- Search Status Dashboard JSON history
