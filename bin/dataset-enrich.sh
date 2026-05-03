#!/usr/bin/env bash
set -euo pipefail

SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"

select_files_by_shard() {
  local files_json="$1"
  python3 - "$files_json" "$SHARD_ID" "$TOTAL_SHARDS" <<'PY'
import json, sys, hashlib
files = json.load(sys.stdin)
shard = int(sys.argv[2])
total = int(sys.argv[3])

selected = []
for f in files:
    # Deterministic shard assignment by filename
    h = int(hashlib.md5(f["path"].encode()).hexdigest(), 16)
    if h % total == shard:
        selected.append(f["path"])

for p in selected:
    print(p)
PY
}

if [[ -n "$SNAPSHOT_FILE" && -f "$SNAPSHOT_FILE" ]]; then
  echo "Using snapshot: $SNAPSHOT_FILE"
  FILES=$(python3 -c "import json; print(json.dumps(json.load(open('$SNAPSHOT_FILE'))['files']))")
  mapfile -t FILE_LIST < <(select_files_by_shard "$FILES")
else
  echo "No snapshot, falling back to live API (rate-limited)"
  # ... existing list_repo_files logic ...
fi

# Download via CDN URLs
for rel_path in "${FILE_LIST[@]}"; do
  url="https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/${rel_path}"
  echo "Processing: $url"
  # Use lib/cdn_download.py or curl with retries; validate sha256 if present
done