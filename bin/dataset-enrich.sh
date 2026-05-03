#!/usr/bin/env bash
set -euo pipefail

# Config
REPO="${HF_DATASET_REPO:-axentx/surrogate-1-training-pairs}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
SHARD_ID="${SHARD_ID:-0}"
MANIFEST="${MANIFEST_JSON:-manifest.json}"
DATEFOLDER="${DATEFOLDER:-$(date +%Y-%m-%d)}"
OUTDIR="batches/public-merged/${DATEFOLDER}"
TIMESTAMP=$(date +%H%M%S)
OUTFILE="${OUTDIR}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

mkdir -p "$(dirname "$OUTFILE")"

# Compute shard assignment from path
should_process() {
  local path="$1"
  local hash
  hash=$(echo -n "$path" | md5sum | cut -c1-8)
  local shard=$(( 0x$hash % TOTAL_SHARDS ))
  [[ $shard -eq $SHARD_ID ]]
}

# Project record to {prompt, response} (best-effort)
project_record() {
  local line="$1"
  local prompt response slug
  # Try common keys; fallback to raw fields
  prompt=$(echo "$line" | python3 -c "
import sys, json
r=json.loads(sys.stdin.read())
print(json.dumps(r.get('prompt') or r.get('input') or r.get('text') or ''))
" 2>/dev/null || echo '""')
  response=$(echo "$line" | python3 -c "
import sys, json
r=json.loads(sys.stdin.read())
print(json.dumps(r.get('response') or r.get('output') or r.get('completion') or ''))
" 2>/dev/null || echo '""')
  slug=$(echo "$line" | python3 -c "
import sys, json, hashlib
r=json.loads(sys.stdin.read())
print(hashlib.md5((r.get('prompt','')+r.get('response','')).encode()).hexdigest()[:12])
" 2>/dev/null || echo 'unknown')
  echo "{\"prompt\":${prompt},\"response\":${response},\"slug\":\"${slug}\",\"shard\":${SHARD_ID}}"
}

# Process manifest entries
if [[ ! -f "$MANIFEST" ]]; then
  echo "MANIFEST not found: $MANIFEST" >&2
  exit 1
fi

# Read paths from manifest (supports both list and object with 'paths')
paths=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data=json.load(f)
if isinstance(data, list):
    for p in data: print(p)
elif isinstance(data, dict) and 'paths' in data:
    for p in data['paths']: print(p)
else:
    # fallback: try to iterate keys
    for p in data: print(p)
" "$MANIFEST")

processed=0
while IFS= read -r relpath; do
  [[ -z "$relpath" ]] && continue
  if ! should_process "$relpath"; then
    continue
  fi

  url="https://huggingface.co/datasets/${REPO}/resolve/main/${relpath}"
  echo "Processing shard ${SHARD_ID}: ${relpath}" >&2

  # Stream download and parse line-by-line (assumes jsonl/parquet handled via python)
  # For parquet files we use python to convert to jsonl projection.
  case "$relpath" in
    *.parquet)
      python3 -c "
import pyarrow.parquet as pq
import sys, json, io, urllib.request
url = sys.argv[1]
import tempfile, os
with tempfile.NamedTemporaryFile(delete=False, suffix='.parquet') as tmp:
    tmp_path = tmp.name
try:
    import urllib.request
    urllib.request.urlretrieve(url, tmp_path)
    table = pq.read_table(tmp_path, columns=['prompt','response'] if set(['prompt','response']).issubset(pq.read_schema(tmp_path).names) else None)
    for batch in table.to_batches(max_chunksize=8192):
        df = batch.to_pandas()
        for _, row in df.iterrows():
            rec = row.to_dict()
            prompt = rec.get('prompt') or rec.get('input') or ''
            response = rec.get('response') or rec.get('output') or ''
            print(json.dumps({'prompt': prompt, 'response': response}))
finally:
    try: os.unlink(tmp_path)
    except: pass
" "$url" 2>/dev/null | while IFS= read -r line; do
        [[ -n "$line" ]] && echo "$line"
      done
      ;;
    *.jsonl|*.json)
      curl -fsSL "$url" | while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        project_record "$line"
      done
      ;;
    *)
      # Generic fallback: try to parse as jsonl
      curl -fsSL "$url" | while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        project_record "$line"
      done
      ;;
  esac

  processed=$((processed + 1))
done <<< "$paths"

echo "Shard ${SHARD_ID} processed ${processed} files" >&2