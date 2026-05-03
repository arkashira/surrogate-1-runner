#!/usr/bin/env bash
set -euo pipefail

HF_TOKEN=${HF_TOKEN:?missing}
HF_REPO=${HF_REPO:-axentx/surrogate-1-training-pairs}
DATE=${DATE:?missing}
SHARD_ID=${SHARD_ID:?missing}
SHARD_TOTAL=${SHARD_TOTAL:-16}
RUN_TS=$(date -u +%Y%m%d-%H%M%S)

OUT_DIR="batches/public-merged/${DATE}"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${RUN_TS}.jsonl"
TMP_DIR=$(mktemp -d)
cleanup() { rm -rf "${TMP_DIR}"; }
trap cleanup EXIT

mkdir -p "$(dirname "${OUT_FILE}")"

# File list: prefer pre-generated artifact; else one API call
FILE_LIST="${TMP_DIR}/file-list.json"
if [[ -f "file-list-${DATE}.json" ]]; then
  cp "file-list-${DATE}.json" "${FILE_LIST}"
else
  echo "Fetching file list for ${DATE}..."
  curl -sSf -H "Authorization: Bearer ${HF_TOKEN}" \
    "https://huggingface.co/api/datasets/${HF_REPO}/tree/public-raw/${DATE}?recursive=false" \
    > "${FILE_LIST}"
fi

mapfile -t FILES < <(jq -r '.[] | select(.type=="file") | .path' < "${FILE_LIST}")

# Deterministic shard assignment
assign_shard() {
  python3 -c "import hashlib; print(int(hashlib.md5(b'$1').hexdigest(), 16) % ${SHARD_TOTAL})"
}

# Process file via CDN (fallback to auth)
process_file() {
  local rel_path=$1
  local cdn_url="https://huggingface.co/datasets/${HF_REPO}/resolve/main/${rel_path}"
  local ext="${rel_path##*.}"
  python3 parse_and_project.py \
    --url "${cdn_url}" \
    --auth-url "https://huggingface.co/datasets/${HF_REPO}/resolve/main/${rel_path}" \
    --token "${HF_TOKEN}" \
    --ext "${ext}" \
    --shard-id "${SHARD_ID}" \
    --shard-total "${SHARD_TOTAL}" \
    --out "${TMP_DIR}/rows.jsonl" \
    --dedup-db "./lib/dedup.db"
}

> "${TMP_DIR}/rows.jsonl"
for f in "${FILES[@]}"; do
  s=$(assign_shard "${f}")
  if [[ "${s}" == "${SHARD_ID}" ]]; then
    echo "Processing: ${f}"
    process_file "${f}" || echo "WARN: failed ${f}"
  fi
done

if [[ -s "${TMP_DIR}/rows.jsonl" ]]; then
  mkdir -p "$(dirname "${OUT_FILE}")"
  cp "${TMP_DIR}/rows.jsonl" "${OUT_FILE}"
  echo "Produced ${OUT_FILE} with $(wc -l < "${OUT_FILE}") rows"
else
  echo "No rows for shard ${SHARD_ID}"
  touch "${OUT_FILE}"
fi

if [[ -s "${OUT_FILE}" ]]; then
  git config user.name "github-actions"
  git config user.email "github-actions@github.com"
  git add "${OUT_FILE}"
  git commit -m "shard${SHARD_ID} public-merged ${DATE} ${RUN_TS}" || true
  git push origin HEAD
fi