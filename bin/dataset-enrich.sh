#!/usr/bin/env bash
set -euo pipefail

export HF_TOKEN="${HF_TOKEN:-}"
export SHARD_ID="${SHARD_ID:-0}"
MANIFEST="${1:-manifest-2026-05-03.json}"
OUT_DIR="batches/public-merged/$(date +%F)"
mkdir -p "$OUT_DIR"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-$(date +%H%M%S).jsonl"

python3 -c "
import json, hashlib, os, sys, time, requests
from lib.dedup import DedupStore

with open('$MANIFEST') as f:
    data = json.load(f)
files = data.get('files', [])

dedup = DedupStore()
shard_id = int('$SHARD_ID')
out_path = '$OUT_FILE'

def assign_shard(slug: str) -> int:
    return int(hashlib.sha256(slug.encode()).hexdigest(), 16) % 16

def project_to_pair(content: bytes, path: str):
    # Replace with actual schema projection for your files.
    # Must return dict with at least {'prompt':..., 'response':...}
    # and optional 'md5' or 'hash' for dedup.
    raise NotImplementedError('Implement projection per schema')

def robust_get(url, max_retries=3, backoff=360):
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=60)
            if resp.status_code == 429:
                if attempt < max_retries - 1:
                    print(f'429 on {url}, sleeping {backoff}s', file=sys.stderr)
                    time.sleep(backoff)
                    continue
                else:
                    resp.raise_for_status()
            resp.raise_for_status()
            return resp.content
        except requests.RequestException:
            if attempt == max_retries - 1:
                raise
            time.sleep(backoff)

with open(out_path, 'w') as out_f:
    for entry in files:
        slug = os.path.splitext(os.path.basename(entry['path']))[0]
        if assign_shard(slug) != shard_id:
            continue

        content = robust_get(entry['cdn_url'])
        try:
            pair = project_to_pair(content, entry['path'])
        except Exception as e:
            print(f'Skip {entry[\"path\"]}: {e}', file=sys.stderr)
            continue

        key = pair.get('md5') or pair.get('hash')
        if not dedup.seen(key):
            out_f.write(json.dumps(pair) + '\n')
            out_f.flush()
print('Shard', shard_id, 'done ->', out_path)
"