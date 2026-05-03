#!/usr/bin/env bash
# ... existing header ...

REPO="${REPO:-axentx/surrogate-1-training-pairs}"
DATE="${DATE:-$(date +%Y-%m-%d)}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"   # optional: snapshot/<date>/file-list.json

# If snapshot provided, use CDN-only fetches; otherwise fallback to datasets API
if [[ -n "$SNAPSHOT_FILE" && -f "$SNAPSHOT_FILE" ]]; then
  echo "Using snapshot: $SNAPSHOT_FILE"
  mapfile -t FILES < <(python3 -c "import json,sys;print('\n'.join([f['path'] for f in json.load(open(sys.argv[1]))['files']]))" "$SNAPSHOT_FILE")
else
  echo "WARNING: No snapshot file provided — falling back to datasets API (may hit rate limits)"
  mapfile -t FILES < <(python3 -c "
from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_files(repo_id='$REPO', repo_type='dataset')
print('\n'.join([f for f in files if f.startswith('$DATE/')]))
")
fi

TOTAL=${#FILES[@]}
echo "Found $TOTAL files for date=$DATE"

# Determine shard slice (same logic as before)
SHARD_ID="${SHARD_ID:-0}"
SHARD_TOTAL="${SHARD_TOTAL:-16}"
if (( SHARD_TOTAL <= 0 )); then SHARD_TOTAL=16; fi
if (( SHARD_ID < 0 || SHARD_ID >= SHARD_TOTAL )); then
  echo "Invalid SHARD_ID=$SHARD_ID (must be 0..$((SHARD_TOTAL-1)))" >&2
  exit 1
fi

# Select deterministic slice by hashing path -> integer mod SHARD_TOTAL
selected_files=()
for f in "${FILES[@]}"; do
  bucket=$(python3 -c "import hashlib; print(int(hashlib.sha256('$f'.encode()).hexdigest(), 16) % $SHARD_TOTAL)")
  if (( bucket == SHARD_ID )); then
    selected_files+=("$f")
  fi
done

echo "Shard $SHARD_ID/$SHARD_TOTAL selected ${#selected_files[@]} files"

# Process selected files
OUTPUT_DIR="batches/public-merged/${DATE}"
mkdir -p "$OUTPUT_DIR"
TS=$(date +%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/shard${SHARD_ID}-${TS}.jsonl"

# Lightweight retry for CDN downloads
cdn_fetch() {
  local url="$1"
  local out="$2"
  local max_retries=3
  for i in $(seq 1 "$max_retries"); do
    if curl -fsSL --retry 2 --retry-delay 1 -o "$out" "$url"; then
      return 0
    fi
    echo "Retry $i/$max_retries for $url" >&2
    sleep $((i * 2))
  done
  return 1
}

# Stream parse each file and project to {prompt,response}
> "$OUTPUT_FILE"
for f in "${selected_files[@]}"; do
  CDN_URL="https://huggingface.co/datasets/${REPO}/resolve/main/${f}"
  TMPFILE=$(mktemp)
  if cdn_fetch "$CDN_URL" "$TMPFILE"; then
    python3 - "$TMPFILE" "$OUTPUT_FILE" <<'PY'
import sys, json, pyarrow as pa, pyarrow.parquet as pq

tmp = sys.argv[1]
out = sys.argv[2]

try:
    table = pq.read_table(tmp, columns=["prompt", "response"])
    rows = table.to_pylist()
except Exception:
    rows = []
    try:
        with open(tmp, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                rows.append(obj)
    except Exception:
        pass

projected = []
for r in rows:
    if isinstance(r, dict) and "prompt" in r and "response" in r:
        projected.append({"prompt": r["prompt"], "response": r["response"]})

with open(out, "a", encoding="utf-8") as f:
    for item in projected:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
PY
    else
      echo "Failed to fetch $f via CDN, skipping" >&2
    fi
    rm -f "$TMPFILE"
  done

echo "Shard $SHARD_ID wrote $OUTPUT_FILE"