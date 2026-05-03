#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... bin/snapshot.sh <repo> <date> [out_dir]
# Example: HF_TOKEN=... bin/snapshot.sh axentx/surrogate-1-training-pairs 2026-04-29 snapshots
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE="${2:-$(date +%Y-%m-%d)}"
OUT_DIR="${3:-snapshots}"
HF_TOKEN="${HF_TOKEN:-}"
API_ROOT="https://huggingface.co/api"

mkdir -p "${OUT_DIR}/${REPO}/${DATE}"

# Single non-recursive tree call to avoid pagination/429
echo "Listing ${REPO} tree for ${DATE} (non-recursive)..."
TREE_JSON=$(curl -sSf \
  -H "Authorization: Bearer ${HF_TOKEN}" \
  "${API_ROOT}/datasets/${REPO}/tree?path=${DATE}&recursive=false")

# Extract file paths (type "file") and sort deterministically
FILES=$(echo "$TREE_JSON" | python3 -c "
import sys, json
tree = json.load(sys.stdin)
paths = [item['path'] for item in tree if item.get('type') == 'file']
for p in sorted(paths):
    print(p)
")

if [ -z "$FILES" ]; then
  echo "No files found for ${DATE} in ${REPO}"
  exit 1
fi

SNAP_TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
MANIFEST="${OUT_DIR}/${REPO}/${DATE}/manifest.json"

python3 -c "
import json, os
repo = os.environ['REPO']
date = os.environ['DATE']
files = os.environ['FILES'].splitlines()
manifest = {
    'repo': repo,
    'date': date,
    'snapshot_ts': os.environ['SNAP_TS'],
    'files': files,
    'count': len(files)
}
with open(os.environ['MANIFEST'], 'w') as f:
    json.dump(manifest, f, indent=2)
print(f'Wrote {len(files)} entries to {os.environ[\"MANIFEST\"]}')
" -- \
  REPO="$REPO" DATE="$DATE" FILES="$FILES" SNAP_TS="$SNAP_TS" MANIFEST="$MANIFEST"

echo "Snapshot created: ${MANIFEST}"