#!/usr/bin/env bash
set -euo pipefail

# Config
REPO="axentx/surrogate-1-training-pairs"
DATE_FOLDER="${DATE_FOLDER:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"          # 0..15 via matrix
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
HF_TOKEN="${HF_TOKEN:-}"
OUT_DIR="work/${DATE_FOLDER}/shard${SHARD_ID}"
FILE_LIST="${OUT_DIR}/files.json"

mkdir -p "${OUT_DIR}"

echo "== Listing ${REPO}/${DATE_FOLDER} (non-recursive) =="
# Single API call: list_repo_tree per folder (no recursion)
python3 - <<PY > "${FILE_LIST}"
import os, json, sys
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get("HF_TOKEN"))
items = api.list_repo_tree(
    repo_id="${REPO}",
    path="${DATE_FOLDER}",
    recursive=False
)
# Keep only files we want to process (parquet/jsonl)
files = [it.rpath for it in items if it.rpath and not it.rpath.endswith("/")]
# Deterministic shard assignment by slug hash
def shard_for(path):
    # path like "2026-05-03/some-slug.parquet"
    slug = path.split("/")[-1].split(".")[0]
    return hash(slug) % ${TOTAL_SHARDS}
sharded = [f for f in files if shard_for(f) == ${SHARD_ID}]
json.dump({"date_folder": "${DATE_FOLDER}", "shard_id": ${SHARD_ID}, "files": sharded}, sys.stdout)
PY

echo "== Shard ${SHARD_ID} will process $(jq '.files | length' "${FILE_LIST}") files =="

# Run enrichment worker (streams via CDN)
python3 bin/lib/fetch_cdn.py \
  --file-list "${FILE_LIST}" \
  --repo "${REPO}" \
  --out-dir "${OUT_DIR}" \
  --hf-token "${HF_TOKEN}"

# Upload shard output (same naming convention)
TS=$(date +%H%M%S)
DEST="batches/public-merged/${DATE_FOLDER}/shard${SHARD_ID}-${TS}.jsonl"
echo "== Uploading to ${REPO}:${DEST} =="
python3 - <<PY
import os, json
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get("HF_TOKEN"))
out_dir = "${OUT_DIR}"
dest = "${DEST}"
output_file = os.path.join(out_dir, "enriched.jsonl")
if os.path.exists(output_file):
    api.upload_file(
        path_or_fileobj=output_file,
        path_in_repo=dest,
        repo_id="${REPO}"
    )
else:
    print("No output file; nothing to upload")
PY