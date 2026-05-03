#!/usr/bin/env bash
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-snapshot/$(date +%Y-%m-%d).json}"

# Resolve file list: snapshot (preferred) or legacy fallback
if [[ -f "$SNAPSHOT_FILE" ]]; then
  echo "Using snapshot: $SNAPSHOT_FILE"
  mapfile -t ALL_FILES < <(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    for p in json.load(f)['files']:
        print(p)
" "$SNAPSHOT_FILE")
else
  echo "WARNING: No snapshot at $SNAPSHOT_FILE — falling back to list_repo_tree (rate-limited)"
  mapfile -t ALL_FILES < <(python3 -c "
from huggingface_hub import HfApi
api = HfApi()
folder = 'public-merged/$(date +%Y-%m-%d)'
items = api.list_repo_tree(repo_id='$REPO', path=folder, recursive=False)
for i in items:
    if i.type == 'file':
        print(i.rfilename)
")
fi

# Deterministic shard assignment by filename hash
shard_files=()
for f in "${ALL_FILES[@]}"; do
  hash=$(python3 -c "import hashlib, sys; print(int(hashlib.md5(sys.argv[1].encode()).hexdigest(), 16))" "$f")
  if (( hash % TOTAL_SHARDS == SHARD_ID )); then
    shard_files+=("$f")
  fi
done

echo "Shard $SHARD_ID processing ${#shard_files[@]} files"

# CDN download with retry/backoff and schema-safe projection
process_file() {
  local rel_path="$1"
  local url="https://huggingface.co/datasets/${REPO}/resolve/main/${rel_path}"
  local tmpfile
  tmpfile=$(mktemp)

  for attempt in 1 2 3; do
    if curl -fsSL --retry 3 --retry-delay 2 --retry-max-time 15 "$url" -o "$tmpfile"; then
      break
    fi
    echo "Retry $attempt for $url"
    sleep $(( RANDOM % 5 + attempt ))
  done

  python3 - "$tmpfile" "$rel_path" <<'PY'
import pyarrow.parquet as pq
import sys, json, os

tmpfile, rel_path = sys.argv[1], sys.argv[2]
try:
    table = pq.read_table(tmpfile, columns=["prompt", "response"])
except Exception:
    try:
        table = pq.read_table(tmpfile)
        if "prompt" not in table.column_names or "response" not in table.column_names:
            raise ValueError("Missing prompt/response columns")
        table = table.select(["prompt", "response"])
    except Exception as e:
        print(f"Skipping {rel_path}: {e}", file=sys.stderr)
        os.unlink(tmpfile)
        sys.exit(0)

df = table.to_pandas()
for _, row in df.iterrows():
    print(json.dumps({"prompt": str(row["prompt"]), "response": str(row["response"])}, ensure_ascii=False))

os.unlink(tmpfile)
PY
}

export -f process_file
export REPO

# Parallelize per-file processing (lightweight), keep ordering non-critical
printf '%s\n' "${shard_files[@]}" | xargs -P 4 -I {} bash -c 'process_file "$@"' _ {} \
  | gzip > "output/shard-${SHARD_ID}-$(date +%H%M%S).jsonl.gz"

# Upload to dataset repo (preserve existing behavior)
DATE=$(date +%Y-%m-%d)
TS=$(date +%H%M%S)
DEST="batches/public-merged/${DATE}/shard-${SHARD_ID}-${TS}.jsonl"

echo "Uploading to ${REPO}:${DEST}"
gzip -d < "output/shard-${SHARD_ID}-${TS}.jsonl.gz" | \
  python3 -c "
import sys
from huggingface_hub import upload_file
upload_file(
    path_or_fileobj=sys.stdin.buffer,
    path_in_repo='$DEST',
    repo_id='$REPO',
    repo_type='dataset',
    commit_message='shard $SHARD_ID'
)"