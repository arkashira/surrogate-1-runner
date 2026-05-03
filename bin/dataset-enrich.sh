#!/usr/bin/env bash
set -euo pipefail

HF_TOKEN="${HF_TOKEN:-}"
REPO="axentx/surrogate-1-training-pairs"
DATE="${DATE:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"
FILE_MANIFEST="${FILE_MANIFEST:-}"
OUT_DIR="batches/public-merged/${DATE}"
TS=$(date +%H%M%S)
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${TS}.jsonl"

mkdir -p "$OUT_DIR"

shard_for() {
  local slug="$1"
  local hash
  hash=$(echo -n "$slug" | sha256sum | tr -d ' -')
  echo $(( 0x${hash:0:8} % 16 ))
}

if [[ -n "$FILE_MANIFEST" && -f "$FILE_MANIFEST" ]]; then
  echo "Using CDN-bypass manifest: $FILE_MANIFEST"
  jq -r '.[] | .path' "$FILE_MANIFEST" | while read -r relpath; do
    slug=$(basename "$relpath" .parquet)
    [[ $(shard_for "$slug") -eq "$SHARD_ID" ]] || continue

    url="https://huggingface.co/datasets/${REPO}/resolve/main/${relpath}"
    tmp=$(mktemp)
    if curl -fsSL "$url" -o "$tmp"; then
      python3 -c "
import json, pyarrow.parquet as pq, sys
try:
  tbl = pq.read_table('$tmp')
  df = tbl.to_pandas()
  prompt_col = next((c for c in df.columns if 'prompt' in c.lower()), df.columns[0])
  response_col = next((c for c in df.columns if 'response' in c.lower() or 'completion' in c.lower()), df.columns[-1])
  for _, row in df.iterrows():
    out = {'prompt': str(row[prompt_col]), 'response': str(row[response_col])}
    print(json.dumps(out, ensure_ascii=False))
except Exception as e:
  sys.stderr.write(f'Parse error {e} for $relpath\\n')
" >> "$OUT_FILE"
    else
      echo "Download failed: $url"
    fi
    rm -f "$tmp"
  done
else
  echo "WARNING: FILE_MANIFEST not provided; falling back to streaming (may hit rate limits)"
  python3 -c "
from datasets import load_dataset
import json
ds = load_dataset('$REPO', split='train', streaming=True)
for ex in ds:
  if hash(ex.get('slug', '')) % 16 == $SHARD_ID:
    print(json.dumps({'prompt': ex.get('prompt', ''), 'response': ex.get('response', '')}, ensure_ascii=False))
" >> "$OUT_FILE"
fi

if [[ -n "$HF_TOKEN" ]]; then
  huggingface-cli upload --repo-type dataset "$REPO" "$OUT_FILE" "$OUT_FILE" --token "$HF_TOKEN"
else
  echo "HF_TOKEN not set; skipping upload"
fi