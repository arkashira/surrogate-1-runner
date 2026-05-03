#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... bin/snapshot.sh <date> [output.json]
# Example: bin/snapshot.sh 2026-05-02 batches/snapshot-2026-05-02.json

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="${2:-batches/snapshot-${DATE}.json}"

mkdir -p "$(dirname "$OUT")"

echo "[$(date -u)] Listing ${REPO}/batches/public-merged/${DATE} ..."

curl -sSf -H "Authorization: Bearer ${HF_TOKEN}" \
  "https://huggingface.co/api/datasets/${REPO}/tree?path=batches/public-merged/${DATE}&recursive=false" \
  > "$OUT.tmp"

# Transform to minimal CDN entries: {path, cdn_url}
python3 -c "
import json, sys
with open('$OUT.tmp') as f:
    tree = json.load(f)
out = []
for node in tree:
    if node.get('type') == 'file':
        out.append({
            'path': node['path'],
            'cdn_url': f'https://huggingface.co/datasets/${REPO}/resolve/main/{node[\"path\"]}'
        })
with open('$OUT', 'w') as f:
    json.dump(out, f, indent=2)
"
rm -f "$OUT.tmp"

echo "[$(date -u)] Snapshot written: $OUT ($(jq length < "$OUT") files)"