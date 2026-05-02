#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Updated: deterministic date partitioning + CDN-only ingestion + idempotent shard paths

set -euo pipefail

# -- config --
REPO="axentx/surrogate-1-training-pairs"
HF_TOKEN="${HF_TOKEN:-}"
SHARD_ID="${SHARD_ID:-0}"        # 0..15
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
DATE_PART=$(date -u +"%Y/%m/%d")
TS=$(date -u +"%H%M%S")
RUN_ID=$(date -u +"%Y%m%d")
OUT_DIR="batches/public-merged/${DATE_PART}"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${RUN_ID}-${TS}.jsonl"
CACHE_DIR=".cache"
FILE_LIST="${CACHE_DIR}/file-list-${RUN_ID}.json"
MAX_RETRIES=5
RETRY_BACKOFF=30

mkdir -p "${CACHE_DIR}" "${OUT_DIR}"

# -- helpers --
log() { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $*"; }

retry() {
  local n=0
  until "$@"; do
    local code=$?
    n=$((n + 1))
    if [ "$n" -ge "$MAX_RETRIES" ]; then
      log "ERROR: command failed after $MAX_RETRIES attempts: $*"
      return $code
    fi
    local sleep_time=$((RETRY_BACKOFF * n))
    log "WARN: command failed (attempt $n/$MAX_RETRIES), retrying in ${sleep_time}s: $*"
    sleep "$sleep_time"
  done
}

# -- pre-flight file list (single API call per run) --
if [ ! -f "${FILE_LIST}" ]; then
  log "Generating pre-flight file list for ${RUN_ID}..."
  # Use recursive=False per top-level folder to avoid 100x pagination; keep list small and deterministic.
  python3 -c "
import json, os
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get('HF_TOKEN'))
# Only list top-level folders/files once; workers will resolve exact paths from this manifest.
tree = api.list_repo_tree(repo_id='${REPO}', path='', recursive=False)
items = [t.rpath for t in tree if t.type == 'file']
open('${FILE_LIST}', 'w').write(json.dumps(items, sort_keys=True))
" || {
    log "ERROR: failed to list repo tree"; exit 1
  }
  log "File list saved to ${FILE_LIST} ($(jq length <"${FILE_LIST}") items)"
fi

# -- deterministic shard assignment --
mapfile -t ALL_FILES < <(jq -r '.[]' "${FILE_LIST}")
TOTAL_FILES=${#ALL_FILES[@]}
if [ "$TOTAL_FILES" -eq 0 ]; then
  log "ERROR: no files to process"; exit 1
fi

# assign files to shards by stable hash of filename
assign_shard() {
  local file="$1"
  # deterministic 0..(TOTAL_SHARDS-1)
  python3 -c "print(abs(hash('${file}')) % ${TOTAL_SHARDS})"
}

# collect shard files
SHARD_FILES=()
for f in "${ALL_FILES[@]}"; do
  s=$(assign_shard "$f")
  if [ "$s" -eq "$SHARD_ID" ]; then
    SHARD_FILES+=("$f")
  fi
done

log "Shard ${SHARD_ID}/${TOTAL_SHARDS} processing ${#SHARD_FILES[@]}/${TOTAL_FILES} files -> ${OUT_FILE}"

# -- CDN-only fetch + schema projection --
process_file() {
  local rel_path="$1"
  local url="https://huggingface.co/datasets/${REPO}/resolve/main/${rel_path}"
  local tmpf
  tmpf=$(mktemp)
  # CDN download (no Authorization header) bypasses API rate limits
  retry curl -fsSL --retry 3 --retry-delay 5 -o "${tmpf}" "${url}" || {
