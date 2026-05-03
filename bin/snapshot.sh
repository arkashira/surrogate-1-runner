#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... ./bin/snapshot.sh axentx/surrogate-1-training-pairs 2026-05-03
set -euo pipefail

REPO="${1:?repo required}"
DATE="${2:?date required (YYYY-MM-DD)}"
OUTDIR="snapshots/${DATE}"
OUTFILE="${OUTDIR}/files.json"

mkdir -p "${OUTDIR}"

# One HF tree API call per date folder (non-recursive).
# Rate-note: this is the only HF API call; CDN downloads do NOT count against limits.
echo "Listing ${REPO} tree for ${DATE}..."
TREE_JSON=$(curl -s \
  -H "Authorization: Bearer ${HF_TOKEN:-}" \
  -H "Content-Type: application/json" \
  "https://huggingface.co/api/datasets/${REPO}/tree?path=${DATE}&recursive=false")

# Extract filenames, sort for determinism, build CDN URLs.
echo "${TREE_JSON}" \
  | python3 -c "
import sys, json, os
tree = json.load(sys.stdin)
items = sorted([item for item in tree if item.get('type') == 'file'], key=lambda x: x['path'])
base = 'https://huggingface.co/datasets/${REPO}/resolve/main'
out = []
for it in items:
    p = it['path']
    out.append({
        'path': p,
        'basename': os.path.basename(p),
        'cdn_url': f'{base}/{p}'
    })
print(json.dumps({'date': '${DATE}', 'repo': '${REPO}', 'files': out}, indent=2))
" > "${OUTFILE}"

echo "Snapshot written to ${OUTFILE}"