#!/usr/bin/env bash
set -euo pipefail

# --
# Config
# --
REPO="datasets/axentx/surrogate-1-training-pairs"
DATE=$(date -u +%Y-%m-%d)
SHARD_ID=${SHARD_ID:-0}
SHARD_TOTAL=${SHARD_TOTAL:-16}
WORKDIR=$(mktemp -d)
cd "$WORKDIR"

# --
# 1) Deterministic date-folder selection (discovery forward progress)
# --
# Pick a date folder from the repo tree so shards advance across time.
# We list top-level date folders once (API), pick by hash mod N.
FOLDERS_JSON=$(curl -sL \
  "https://huggingface.co/api/datasets/${REPO}/tree?recursive=false" \
  | jq -r '.[] | select(.type=="directory") | .path' \
  | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' \
  | sort)

FOLDER_COUNT=$(echo "$FOLDERS_JSON" | wc -l)
if [[ "$FOLDER_COUNT" -eq 0 ]]; then
  echo "No date folders found"
  exit 1
fi

# Deterministic choice: hash of today's date mod folder count
HASH=$(echo -n "$DATE" | sha256sum | tr -d ' -')
INDEX=$((0x${HASH:0:8} % FOLDER_COUNT))
TARGET_FOLDER=$(echo "$FOLDERS_JSON" | sed -n "$((INDEX+1))p")
echo "Selected date folder: $TARGET_FOLDER"

# --
# 2) Produce file list once (API) -> embed for CDN-only workers
# --
FILE_LIST="filelist.json"
if [[ ! -f "$FILE_LIST" ]]; then
  curl -sL \
    "https://huggingface.co/api/datasets/${REPO}/tree?recursive=false&path=${TARGET_FOLDER}" \
    | jq '[.[] | select(.type=="file") | .path]' > "$FILE_LIST"
fi

TOTAL_FILES=$(jq 'length' "$FILE_LIST")
if [[ "$TOTAL_FILES" -eq 0 ]]; then
  echo "No files in $TARGET_FOLDER"
  exit 0
fi

# --
# 3) Deterministic shard slicing (stable across runs)
# --
SLICE_FILES=$(jq -r --argjson shard "$SHARD_ID" --argjson total "$SHARD_TOTAL" \
  'to_entries | map(select((.key % $total) == $shard)) | map(.value) | .[]' \
  "$FILE_LIST")

if [[ -z "$SLICE_FILES" ]]; then
  echo "No files assigned to shard $SHARD_ID"
  exit 0
fi

# --
# 4) Process assigned files via CDN (no Authorization header)
# --
OUTDIR="out-shard-$SHARD_ID"
mkdir -p "$OUTDIR"

process_file() {
  local relpath="$1"
  local outfile="$OUTDIR/$(basename "$relpath" .parquet).jsonl"
  # Download via CDN (no auth) -> project to {prompt,response} -> normalize
  curl -sL "https://huggingface.co/datasets/${REPO}/resolve/main/${relpath}" -o "${relpath##*/}"
  # Lightweight projection: assumes parquet -> jsonl conversion available
  python3 -c "
import pyarrow.parquet as pq, json, sys
try:
    tbl = pq.read_table(sys.argv[1], columns=['prompt','response'])
    for rec in tbl.to_pylist():
        if rec.get('prompt') and rec.get('response'):
            print(json.dumps({'prompt': rec['prompt'], 'response': rec['response']}))
except Exception:
    pass
" "${relpath##*/}" >> "$outfile"
  rm -f "${relpath##*/}"
}

export -f process_file
export REPO OUTDIR
echo "$SLICE_FILES" | xargs -P 4 -I {} bash -c 'process_file "$@"' _ {}

# --
# 5) Upload shard output (avoid collisions: shard+timestamp)
# --
TIMESTAMP=$(date -u +%H%M%S)
DEST="batches/public-merged/${DATE}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"
cat "$OUTDIR"/*.jsonl | \
  python3 /opt/axentx/surrogate-1/lib/dedup.py --input /dev/stdin --output - | \
  curl -sL -X PUT \
    -H "Authorization: Bearer ${HF_TOKEN}" \
    -H "Content-Type: application/jsonl" \
    --data-binary @- \
    "https://huggingface.co/api/datasets/${REPO}/uploads/${DEST}?overwrite=true"

echo "Uploaded $DEST"