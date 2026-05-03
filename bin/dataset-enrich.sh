#!/usr/bin/env bash
# CDN-only ingestion; no HF API auth during streaming
set -euo pipefail

REPO="${REPO:-axentx/surrogate-1-training-pairs}"
DATE="${DATE:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
MANIFEST="${MANIFEST:-manifest-${DATE}.json}"
OUT_DIR="${OUT_DIR:-output}"
TMP_DIR="${TMP_DIR:-/tmp/surrogate-ingest}"

mkdir -p "$OUT_DIR" "$TMP_DIR"

# Validate manifest
if [[ ! -f "$MANIFEST" ]]; then
  echo "ERROR: Manifest $MANIFEST not found. Generate with bin/gen-manifest.sh"
  exit 1
fi

# Load file list from manifest (deterministic)
mapfile -t ALL_FILES < <(
  python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for fn in sorted(data['files']):
    print(fn)
" "$MANIFEST"
)

TOTAL_FILES="${#ALL_FILES[@]}"
if [[ "$TOTAL_FILES" -eq 0 ]]; then
  echo "No files in manifest for $DATE"
  exit 0
fi

# Deterministic shard assignment (stable by filename)
mapfile -t MY_FILES < <(
  for f in "${ALL_FILES[@]}"; do
    HASH=$(echo -n "$f" | md5sum | awk '{print $1}')
    SHARD=$(( 0x${HASH:0:8} % TOTAL_SHARDS ))
    if [[ "$SHARD" -eq "$SHARD_ID" ]]; then
      echo "$f"
    fi
  done
)

echo "Shard $SHARD_ID/$TOTAL_SHARDS processing ${#MY_FILES[@]} files (out of $TOTAL_FILES total)"

# Process via CDN only
for REL_PATH in "${MY_FILES[@]}"; do
  FILENAME=$(basename "$REL_PATH")
  CDN_URL="https://huggingface.co/datasets/${REPO}/resolve/main/${REL_PATH}"
  TMP_FILE="${TMP_DIR}/${FILENAME}.dl"

  echo "Downloading ${REL_PATH} via CDN..."
  curl -fsSL --retry 3 --retry-delay 5 -o "$TMP_FILE" "$CDN_URL"

  # Project to {prompt,response} at parse time
  OUT_TMP="${TMP_DIR}/${FILENAME}.projected.jsonl"
  python3 - "$TMP_FILE" "$OUT_TMP" <<'PY'
import sys, json, pyarrow.parquet as pq

src, dst = sys.argv[1], sys.argv[2]

def normalize(obj):
    prompt = obj.get("prompt") or obj.get("input") or obj.get("text") or ""
    response = obj.get("response") or obj.get("output") or obj.get("completion") or ""
    if not prompt and not response:
        return None
    return {"prompt": str(prompt), "response": str(response)}

rows = []
if src.endswith(".parquet"):
    tbl = pq.read_table(src)
    schema_names = [f.name for f in tbl.schema]
    # Read all rows; normalize will pick fields
    for batch in tbl.to_batches():
        for row in batch.to_pylist():
            rows.append(normalize(row))
elif src.endswith(".jsonl"):
    with open(src, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(normalize(json.loads(line)))
            except Exception:
                continue
elif src.endswith(".json"):
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        rows = [normalize(obj) for obj in data]
    else:
        rows = [normalize(data)]

rows = [r for r in rows if r is not None]
with open(dst, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
PY

  if [[ -s "$OUT_TMP" ]]; then
    cat "$OUT_TMP" >> "${OUT_DIR}/shard${SHARD_ID}-projected.jsonl"
  fi

  rm -f "$TMP_FILE" "$OUT_TMP"
done

echo "Shard $SHARD_ID complete"