#!/usr/bin/env bash
set -euo pipefail

# Surrogate-1 CDN-bypass ingestion worker
# Usage: ./dataset-enrich.sh <date> <shard_id> <total_shards>
# Example: ./dataset-enrich.sh 2026-05-03 0 16

DATE="${1:-$(date +%Y-%m-%d)}"
SHARD_ID="${2:-0}"
TOTAL_SHARDS="${3:-16}"
REPO="axentx/surrogate-1-training-pairs"
FOLDER="public-raw/${DATE}"
OUT_DIR="output/${DATE}"
TIMESTAMP=$(date +%H%M%S)
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

mkdir -p "${OUT_DIR}"

echo "[$(date)] Worker shard=${SHARD_ID}/${TOTAL_SHARDS} date=${DATE}"
echo "[$(date)] Listing folder (non-recursive): ${FOLDER}"

# Use huggingface_hub to list only immediate files in folder (no recursion)
# This avoids paginated list_repo_files and stays under API limits.
python3 - <<PY > /tmp/filelist.json
import os, json
from huggingface_hub import list_repo_tree

repo = os.environ.get("REPO", "${REPO}")
folder = os.environ.get("FOLDER", "${FOLDER}")

# Non-recursive tree listing for one folder
tree = list_repo_tree(repo=repo, path=folder, recursive=False)
files = [f.rfilename for f in tree if f.type == "file"]
json.dump(files, open("/tmp/filelist.json", "w"))
print(json.dumps(files))
PY

FILELIST=$(cat /tmp/filelist.json)
FILE_COUNT=$(echo "${FILELIST}" | jq length)
echo "[$(date)] Found ${FILE_COUNT} files in ${FOLDER}"

# Determine shard slice by deterministic hash of filename
python3 - <<PY
import json, hashlib, os, sys

files = json.loads(os.environ["FILELIST"])
shard_id = int(os.environ["SHARD_ID"])
total_shards = int(os.environ["TOTAL_SHARDS"])
out_file = os.environ["OUT_FILE"]

def shard_for(fname, total):
    # Deterministic, stable across runs
    h = int(hashlib.sha256(fname.encode()).hexdigest(), 16)
    return h % total

selected = [f for f in files if shard_for(f, total_shards) == shard_id]
print(f"Shard {shard_id}/{total_shards} processing {len(selected)} files")

# Pass selected files to the enrichment script via env
os.environ["SELECTED_FILES"] = json.dumps(selected)
PY

SELECTED_FILES=$(python3 -c "import os,json; print(os.environ.get('SELECTED_FILES','[]'))")

# Run enrichment using CDN-only fetches
python3 bin/enrich_worker.py \
  --repo "${REPO}" \
  --date "${DATE}" \
  --shard-id "${SHARD_ID}" \
  --total-shards "${TOTAL_SHARDS}" \
  --out "${OUT_FILE}" \
  --filelist "${SELECTED_FILES}"

echo "[$(date)] Wrote ${OUT_FILE}"