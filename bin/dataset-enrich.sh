#!/usr/bin/env bash
# dataset-enrich.sh
# Usage: SHARD_ID=0 NUM_SHARDS=16 [MANIFEST=shard-manifest.json] ./dataset-enrich.sh
set -euo pipefail

SHARD_ID="${SHARD_ID:-0}"
NUM_SHARDS="${NUM_SHARDS:-16}"
MANIFEST="${MANIFEST:-}"
HF_TOKEN="${HF_TOKEN:-}"
REPO_DST="axentx/surrogate-1-training-pairs"
DATE="$(date +%Y-%m-%d)"
TS="$(date +%H%M%S)"
OUT="shard-${SHARD_ID}-${TS}.jsonl"

echo "[$(date)] Shard ${SHARD_ID}/${NUM_SHARDS} starting"

if [ -n "$MANIFEST" ] && [ -f "$MANIFEST" ]; then
  echo "[$(date)] Using CDN manifest $MANIFEST"
  # Select deterministic shard of CDN entries
  mapfile -t ENTRIES < <(jq -r --argjson sid "$SHARD_ID" --argjson n "$NUM_SHARDS" '
    to_entries
    | map(select(.key % $n == $sid))
    | .[].value | @base64
  ' < "$MANIFEST")

  python3 -c "
import json, base64, sys
from lib.cdn_stream import cdn_stream
entries = [json.loads(base64.b64decode(e).decode()) for e in sys.argv[1:]]
for obj in cdn_stream(entries):
    print(json.dumps(obj, ensure_ascii=False))
" "${ENTRIES[@]}" > "$OUT"

else
  echo "[$(date)] No manifest; falling back to HF dataset streaming"
  python3 -c "
from datasets import load_dataset
import json, os, hashlib
shard = int(os.environ['SHARD_ID'])
n = int(os.environ['NUM_SHARDS'])
ds = load_dataset('${REPO_DST}', split='train', streaming=True)
for i, ex in enumerate(ds):
    if i % n != shard:
        continue
    prompt = ex.get('prompt') or ex.get('input') or ex.get('question')
    response = ex.get('response') or ex.get('output') or ex.get('answer')
    if prompt is None or response is None:
        continue
    print(json.dumps({'prompt': prompt, 'response': response, '_source': 'hf_stream'}, ensure_ascii=False))
" > "$OUT"
fi

# Dedup + upload (existing logic via lib/dedup.py)
if [ -s "$OUT" ]; then
  python3 lib/dedup.py "$OUT" "batches/public-merged/${DATE}/${OUT}"
  huggingface-cli upload --token "$HF_TOKEN" "$REPO_DST" "batches/public-merged/${DATE}/${OUT}" --repo-type dataset
  echo "[$(date)] Uploaded $OUT"
else
  echo "[$(date)] No records for shard ${SHARD_ID}"
fi