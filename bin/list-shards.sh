#!/usr/bin/env bash
# list-shards.sh
# Usage: HF_TOKEN=... ./list-shards.sh [date]
# Outputs: shard-manifest.json
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="shard-manifest.json"

echo "[$(date)] Listing ${REPO} folder: ${DATE}/ ..."

# Single API call: list top-level folder (non-recursive)
FILES=$(huggingface-cli api --token "$HF_TOKEN" list-files-repo --repo-type dataset "$REPO" --path "$DATE" --recursive false 2>/dev/null || true)

if [ -z "$FILES" ]; then
  echo "[$(date)] No files found for ${DATE}. Trying fallback tree..."
  FILES=$(huggingface-cli api --token "$HF_TOKEN" list-files-repo --repo-type dataset "$REPO" --path "$DATE" --recursive false --json 2>/dev/null || echo '[]')
fi

# Build manifest with CDN URLs
echo "$FILES" | jq -r '
  map(select(.path | endswith(".jsonl") or endswith(".parquet"))) |
  map({
    path: .path,
    cdn_url: ("https://huggingface.co/datasets/" + "'"$REPO"'" + "/resolve/main/" + .path)
  })
' > "$OUT"

echo "[$(date)] Wrote $(jq length "$OUT") files to $OUT"