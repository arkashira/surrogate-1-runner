#!/usr/bin/env bash
set -euo pipefail

# Usage: dataset-enrich.sh <date> <shard_id> <total_shards>
# Example: dataset-enrich.sh 2026-05-03 0 16

DATE="${1:-$(date +%Y-%m-%d)}"
SHARD_ID="${2:-${SHARD_ID:-0}}"
TOTAL_SHARDS="${3:-${TOTAL_SHARDS:-16}}"
HF_REPO="${HF_REPO:-datasets/axentx/surrogate-1-training-pairs}"
HF_TOKEN="${HF_TOKEN:?HF_TOKEN required}"
OUT_DIR="batches/public-merged/${DATE}"
TIMESTAMP=$(date +%H%M%S)
OUTPUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

mkdir -p "$(dirname "${OUTPUT_FILE}")"

echo "[$(date)] Shard ${SHARD_ID}/${TOTAL_SHARDS} | Date ${DATE}"
echo "Listing ${HF_REPO} tree for ${DATE}..."

# Single non-recursive tree call per date folder (avoids recursive pagination)
TREE_JSON=$(python3 -c "
import json, os, sys
from huggingface_hub import HfApi
api = HfApi(token=os.environ['HF_TOKEN'])
items = api.list_repo_tree(
    repo_id=os.environ['HF_REPO'],
    path='${DATE}',
    repo_type='dataset',
    recursive=False
)
# Keep only files (ignore subfolders)
files = [i for i in items if i.type == 'file']
print(json.dumps([f.rfilename for f in files]))
" 2>/dev/null || python3 -c "
# Fallback: if HF SDK not available, use raw API (still one call)
import json, os, sys, urllib.request
token = os.environ['HF_TOKEN']
url = f'https://huggingface.co/api/datasets/{os.environ[\"HF_REPO\"]}/tree?path=${DATE}&recursive=false'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as resp:
    items = json.load(resp)
files = [i['path'] for i in items if i['type'] == 'file' and i['path'].startswith('${DATE}/')]
print(json.dumps(files))
")

# Deterministic shard assignment by slug hash
FILTERED=$(python3 -c "
import json, hashlib, sys
files = json.loads(sys.stdin.read())
shard_id = int(${SHARD_ID})
total = int(${TOTAL_SHARDS})
selected = []
for f in files:
    # Use filename as slug; deterministic modulo shard
    slug = f.split('/')[-1]
    h = int(hashlib.sha256(slug.encode()).hexdigest(), 16)
    if (h % total) == shard_id:
        selected.append(f)
print(json.dumps(selected))
" <<< "${TREE_JSON}")

echo "Selected $(echo "${FILTERED}" | python3 -c "import sys,json;print(len(json.load(sys.stdin)))") files for shard ${SHARD_ID}"

# Emit CDN-only URL list for downstream loader (zero API calls during fetch)
python3 -c "
import json, sys, os
files = json.loads(sys.stdin.read())
repo = os.environ['HF_REPO']
urls = [f'https://huggingface.co/datasets/{repo}/resolve/main/{f}' for f in files]
with open('${OUT_DIR}/shard${SHARD_ID}-urls.json', 'w') as f:
    json.dump(urls, f)
" <<< "${FILTERED}"

# Stream selected files via CDN and normalize to {prompt,response}
python3 bin/process_shard.py \
  --urls-file "${OUT_DIR}/shard${SHARD_ID}-urls.json" \
  --output "${OUTPUT_FILE}" \
  --dedup-db "lib/dedup.sqlite"

echo "Writing ${OUTPUT_FILE}"
echo "Uploading to HF dataset..."

git config user.name "github-actions"
git config user.email "actions@github.com"
git add "${OUTPUT_FILE}" "${OUT_DIR}/shard${SHARD_ID}-urls.json" || true
git commit -m "shard${SHARD_ID} ${DATE} ${TIMESTAMP}" || true
git push origin HEAD

echo "[$(date)] Shard ${SHARD_ID} done"