#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Runs in GitHub Actions (16-shard matrix)
set -euo pipefail

# Config
REPO="axentx/surrogate-1-training-pairs"
DATE_FOLDER="${DATE_FOLDER:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
HF_TOKEN="${HF_TOKEN:-}"
OUT_DIR="./output"
mkdir -p "$OUT_DIR"

# 1. Accept pre-listed file list (embedded or downloaded)
FILE_LIST="${FILE_LIST:-/tmp/file-list-${DATE_FOLDER}.json}"

# If file list not provided, fetch once per shard start (fallback)
if [[ ! -f "$FILE_LIST" ]]; then
  echo "[$SHARD_ID] Fetching file list for $DATE_FOLDER..."
  URL="https://huggingface.co/api/datasets/${REPO}/tree?path=${DATE_FOLDER}&recursive=false"
  if [[ -n "$HF_TOKEN" ]]; then
    curl -sL -H "Authorization: Bearer ${HF_TOKEN}" "$URL" -o "$FILE_LIST"
  else
    curl -sL "$URL" -o "$FILE_LIST"
  fi
fi

# Extract file paths
mapfile -t ALL_FILES < <(jq -r '.[] | select(.type=="file") | .path' "$FILE_LIST")
TOTAL_FILES=${#ALL_FILES[@]}

if [[ $TOTAL_FILES -eq 0 ]]; then
  echo "[$SHARD_ID] No files found for $DATE_FOLDER, exiting."
  exit 0
fi

# 2. Deterministic shard assignment: hash(path) mod TOTAL_SHARDS
process_file() {
  local filepath="$1"
  local slug_hash
  slug_hash=$(echo -n "$filepath" | md5sum | cut -c1-8)
  local shard_assign=$(( 0x${slug_hash} % TOTAL_SHARDS ))
  [[ $shard_assign -eq $SHARD_ID ]]
}

# 3. Filter to this shard's files
SHARD_FILES=()
for f in "${ALL_FILES[@]}"; do
  if process_file "$f"; then
    SHARD_FILES+=("$f")
  fi
done

echo "[$SHARD_ID] Processing ${#SHARD_FILES[@]}/${TOTAL_FILES} files (shard ${SHARD_ID}/${TOTAL_SHARDS})"

# 4. Process each file: CDN download + schema projection
TIMESTAMP=$(date +%H%M%S)
OUTPUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

process_and_project() {
  local filepath="$1"
  local cdn_url="https://huggingface.co/datasets/${REPO}/resolve/main/${filepath}"
  local tmp_file
  tmp_file=$(mktemp)

  if curl -sL -f "$cdn_url" -o "$tmp_file"; then
    python3 -c "
import sys, json, pyarrow.parquet as pq
try:
    table = pq.read_table('$tmp_file')
    prompt = table['prompt'].to_pylist() if 'prompt' in table.column_names else [None] * len(table)
    response = table['response'].to_pylist() if 'response' in table.column_names else [None] * len(table)
    for p, r in zip(prompt, response):
        if p is not None and r is not None:
            print(json.dumps({'prompt': p, 'response': r, 'source_file': '$filepath'}))
except Exception:
    pass
" >> "$OUTPUT_FILE" 2>/dev/null || true
    rm -f "$tmp_file"
  else
    echo "[$SHARD_ID] CDN download failed: $filepath" >&2
    rm -f "$tmp_file"
  fi
}

export -f process_and_project
export OUTPUT_FILE

# Parallel within shard
printf '%s\n' "${SHARD_FILES[@]}" | xargs -P 4 -I {} bash -c 'process_and_project "$@"' _ {}

# 5. Upload to HF dataset repo (git-based, deterministic filenames)
if [[ -s "$OUTPUT_FILE" ]]; then
  LINES=$(wc -l < "$OUTPUT_FILE")
  echo "[$SHARD_ID] Produced $LINES pairs -> shard${SHARD_ID}-${TIMESTAMP}.jsonl"

  if [[ -n "$HF_TOKEN" ]]; then
    git config --global user.email "runner@axentx.io"
    git config --global user.name "surrogate-1-runner"

    DATASET_DIR="/tmp/dataset-repo"
    rm -rf "$DATASET_DIR"
    git clone --depth 1 "https://${HF_TOKEN}@huggingface.co/datasets/${REPO}" "$DATASET_DIR"

    DEST_DIR="${DATASET_DIR}/batches/public-merged/${DATE_FOLDER}"
    mkdir -p "$DEST_DIR"
    cp "$OUTPUT_FILE" "${DEST_DIR}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

    cd "$DATASET_DIR"
    git add "batches/public-merged/${DATE_FOLDER}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"
    git commit -m "shard${SHARD_ID}: ${TIMESTAMP} - ${LINES} pairs"
    git push origin main

    echo "[$SHARD_ID] Commit pushed successfully"
  else
    echo "[$SHARD_ID] No HF_TOKEN, skipping upload (dry-run)"
  fi
else
  echo "[$SHARD_ID] No valid pairs produced"
fi