#!/usr/bin/env bash
# bin/dataset-enrich.sh
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
FILE_LIST="${FILE_LIST:-}"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%H%M%S)
OUTPUT="batches/public-merged/${DATE}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

echo "Starting shard ${SHARD_ID}/${TOTAL_SHARDS} | ${DATE} ${TIMESTAMP}"
mkdir -p "$(dirname "$OUTPUT")"

if [[ -n "$FILE_LIST" && -f "$FILE_LIST" ]]; then
    echo "Using pre-generated file list: $FILE_LIST"
    python - <<PY
import json, hashlib, sys
import requests
import pyarrow.parquet as pq
import pyarrow as pa

with open("$FILE_LIST") as f:
    files = json.load(f)

def shard_for(slug: str, total: int) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % total

shard_id = int("$SHARD_ID")
total_shards = int("$TOTAL_SHARDS")
output_path = "$OUTPUT"
processed = 0

for entry in files:
    slug = entry["path"].rsplit(".", 1)[0]
    if shard_for(slug, total_shards) != shard_id:
        continue
    try:
        resp = requests.get(entry["cdn_url"], timeout=30)
        resp.raise_for_status()
        if entry["path"].endswith(".parquet"):
            tbl = pq.read_table(pa.BufferReader(resp.content))
            df = tbl.to_pandas()
            prompt_col = next((c for c in df.columns if "prompt" in c.lower()), None)
            response_col = next((c for c in df.columns if "response" in c.lower()), None)
            if prompt_col and response_col:
                for _, row in df.iterrows():
                    print(json.dumps({"prompt": str(row[prompt_col]), "response": str(row[response_col])}))
                    processed += 1
        elif entry["path"].endswith(".jsonl"):
            for line in resp.text.strip().split('\n'):
                if line:
                    data = json.loads(line)
                    prompt = data.get("prompt") or data.get("input") or ""
                    response = data.get("response") or data.get("output") or ""
                    if prompt and response:
                        print(json.dumps({"prompt": str(prompt), "response": str(response)}))
                        processed += 1
    except Exception as e:
        print(f"Error processing {entry['path']}: {e}", file=sys.stderr)
        continue

print(f"Processed {processed} pairs for shard {shard_id}", file=sys.stderr)
PY
else
    echo "WARNING: No FILE_LIST provided, falling back to streaming (rate-limited)"
    python -c "
from datasets import load_dataset
import json, hashlib
ds = load_dataset('$REPO', split='train', streaming=True)
for item in ds:
    slug = item.get('source', 'unknown')
    if int(hashlib.md5(slug.encode()).hexdigest(), 16) % $TOTAL_SHARDS == $SHARD_ID:
        print(json.dumps({'prompt': item.get('prompt',''), 'response': item.get('response','')}))
" > "$OUTPUT"
fi

echo "Shard ${SHARD_ID} complete: ${OUTPUT}"