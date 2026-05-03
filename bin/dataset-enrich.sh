#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Deterministic shard worker with CDN-bypass ingestion.
set -euo pipefail

# -- config --
REPO="axentx/surrogate-1-training-pairs"
BASE_URL="https://huggingface.co/datasets/${REPO}/resolve/main"
WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEDUP_PY="${WORKDIR}/lib/dedup.py"

HF_TOKEN="${HF_TOKEN:-}"
SHARD_ID="${SHARD_ID:?required}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
DATE="${INGEST_DATE:-$(date -u +%Y-%m-%d)}"
TIMESTAMP="$(date -u +%H%M%S)"
OUT_DIR="${WORKDIR}/out/batches/public-merged/${DATE}"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"
SUMMARY_FILE="${OUT_DIR}/shard${SHARD_ID}-${TIMESTAMP}-summary.json"

FILE_LIST="${WORKDIR}/file-list-${DATE}.json"

mkdir -p "${OUT_DIR}"

log() { echo "[$(date -u +%H:%M:%S)] $*"; }

# -- helpers --
should_process() {
  local slug="$1"
  local hash
  hash=$(echo -n "$slug" | md5sum | cut -c1-8)
  hash=$((0x${hash} % TOTAL_SHARDS))
  [[ $hash -eq $SHARD_ID ]]
}

download_cdn() {
  local path="$1"
  local out="$2"
  curl -fL --retry 3 --retry-delay 5 \
    "${BASE_URL}/${path}" -o "${out}"
}

process_file() {
  local relpath="$1"
  local tmp
  tmp="$(mktemp)"
  if download_cdn "${relpath}" "${tmp}"; then
    python3 "${DEDUP_PY}" --input "${tmp}" --shard-id "${SHARD_ID}" --out "${OUT_FILE}" || true
  else
    log "WARN: failed to download ${relpath}"
    return 1
  fi
  rm -f "${tmp}"
}

# -- main --
log "Starting shard ${SHARD_ID}/${TOTAL_SHARDS} for ${DATE}"

# Idempotency: if any existing shard output exists for this run pattern, skip processing.
# (We still produce a fresh timestamped file each run, but avoid re-processing same list.)
if compgen -G "${OUT_DIR}/shard${SHARD_ID}-*.jsonl" > /dev/null 2>&1; then
  log "Found existing shard outputs in ${OUT_DIR}; skipping processing (idempotency)."
  exit 0
fi

if [[ -f "${FILE_LIST}" ]]; then
  log "Using pre-flight file list ${FILE_LIST}"
  mapfile -t FILES < <(python3 -c "
import json, sys
with open('${FILE_LIST}') as f:
    data=json.load(f)
for fn in data.get('files', []):
    print(fn)
")
  if [[ ${#FILES[@]} -eq 0 ]]; then
    log "WARN: file list empty; nothing to process."
    echo '{"shard_id":'${SHARD_ID}',"date":"'${DATE}'","status":"no_files","processed":0,"skipped":0,"errors":0}' > "${SUMMARY_FILE}"
    exit 0
  fi
else
  log "WARN: no file list ${FILE_LIST}; skipping (prefer pre-flight list)."
  echo '{"shard_id":'${SHARD_ID}',"date":"'${DATE}'","status":"no_file_list","processed":0,"skipped":0,"errors":0}' > "${SUMMARY_FILE}"
  exit 0
fi

TOTAL=${#FILES[@]}
PROCESSED=0
ERRORS=0

for f in "${FILES[@]}"; do
  slug="${f##*/}"
  slug="${slug%.*}"
  if should_process "${slug}"; then
    log "Processing ${f}"
    if process_file "${f}"; then
      PROCESSED=$((PROCESSED+1))
    else
      ERRORS=$((ERRORS+1))
    fi
  fi
done

log "Shard ${SHARD_ID} finished. Output: ${OUT_FILE}"
echo '{
  "shard_id": '${SHARD_ID}',
  "date": "'${DATE}'",
  "status": "done",
  "processed": '${PROCESSED}',
  "total_candidates": '${TOTAL}',
  "errors": '${ERRORS}',
  "output_file": "'${OUT_FILE}'",
  "generated_at": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}' > "${SUMMARY_FILE}"