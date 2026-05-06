#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${HOME}/.codex/memories/google-search-seo-watch.env"
if [[ -f "${ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

export TELEGRAM_TRENDS_THREAD_ID="${TELEGRAM_TRENDS_THREAD_ID:-7}"

/usr/bin/python3 /home/googleupdate/.codex/skills/google-search-seo-watch/scripts/google_trends_finance_watch.py \
  --state "${HOME}/.codex/memories/google-trends-finance-state.json" \
  --send-telegram \
  "$@"
