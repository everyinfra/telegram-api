#!/usr/bin/env bash
# Telegram API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the Telegram API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh profile durov       # 频道用户名 / a channel username
#   bash examples/curl.sh channel_posts durov
#   bash examples/curl.sh search bitcoin      # 关键词 / a keyword
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <profile|channel_posts|search> <value>"}
value=${2:?"value: a channel username or a keyword"}

case "$action" in
  profile | channel_posts) params="{\"username\":\"$value\"}" ;;
  search)                  params="{\"keyword\":\"$value\"}" ;;
  *) echo "unknown action: $action (use profile, channel_posts or search)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"telegram\",\"action\":\"$action\",\"params\":$params}"
echo
