#!/usr/bin/env bash
# ... existing header ...
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE_FOLDER="${DATE_FOLDER:-$(date -u +%Y-%m-%d)}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"

# Determine file list
if [[ -n "${SNAPSHOT_FILE}" && -f "${SNAPSHOT_FILE}" ]]; then
  echo "Using snapshot: ${SNAPSHOT_FILE}"
  mapfile -t ALL_FILES < <(jq -r '.files[]' "${SNAPSHOT_FILE}")
else
  echo "No snapshot provided; listing repo tree (non-recursive) for public-merged/${DATE_FOLDER}"
  mapfile -t ALL_FILES < <(
    python3 -c "
import sys
from huggingface_hub import HfApi
api = HfApi()
tree = api.list_repo_tree('${REPO}', path='public-merged/${DATE_FOLDER}', recursive=False)
for item in tree:
    if item.type == 'file' and item.path.lower().endswith(('.parquet','.jsonl')):
        print(item.path)
"
  )
fi

# Shard assignment (unchanged)
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"

process_file() {
  local rel_path="$1"
  local cdn_url="https://huggingface.co/datasets/${REPO}/resolve/main/${rel_path}"
  # Download via CDN (no auth header) and process
  # ... existing normalization + dedup logic ...
}

for f in "${ALL_FILES[@]}"; do
  # Deterministic shard selection
  slug=$(basename "$f" | sed 's/\.[^.]*$//')
  bucket=$(( $(echo -n "$slug" | md5sum | cut -c1-8) % TOTAL_SHARDS ))
  if [[ "$bucket" -eq "$SHARD_ID" ]]; then
    process_file "$f"
  fi
done