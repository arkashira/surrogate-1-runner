#!/usr/bin/env bash
set -euo pipefail

# Config
REPO="axentx/surrogate-1-training-pairs"
HF_TOKEN="${HF_TOKEN:-}"
SHARD_ID="${SHARD_ID:-0}"          # 0..15 via matrix
TODAY=$(date -u +%Y-%m-%d)
OUT_DIR="batches/public-merged/${TODAY}"
mkdir -p "${OUT_DIR}"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-$(date -u +%H%M%S).jsonl"

# 1) Pre-flight: list today's folder once (non-recursive)
#    Uses HF API (counts toward rate limit) — run once per workflow.
echo "Listing ${REPO} folder for ${TODAY}..."
if [ -n "${HF_TOKEN}" ]; then
  AUTH_HEADER="Authorization: Bearer ${HF_TOKEN}"
else
  AUTH_HEADER=""
fi

# Save file list for all shards to reuse (optional: commit to repo or pass via artifact)
FILE_LIST="file-list-${TODAY}.json"
if [ ! -f "${FILE_LIST}" ]; then
  curl -sSf -H "${AUTH_HEADER}" \
    "https://huggingface.co/api/datasets/${REPO}/tree?path=${TODAY}&recursive=false" \
    | jq -r '[.tree[] | select(.type=="blob") | .path] | sort' > "${FILE_LIST}"
fi

# 2) Assign deterministic shard files
mapfile -t ALL_FILES < <(jq -r '.[]' "${FILE_LIST}")
SHARD_FILES=()
for f in "${ALL_FILES[@]}"; do
  # Deterministic hash-based shard assignment
  HASH=$(echo -n "${f}" | sha256sum | awk '{print strtonum("0x" substr($1,1,8))}')
  if (( HASH % 16 == SHARD_ID )); then
    SHARD_FILES+=("${f}")
  fi
done

echo "Shard ${SHARD_ID}: processing ${#SHARD_FILES[@]} files."

# 3) Process each assigned file via CDN (no auth header)
for rel_path in "${SHARD_FILES[@]}"; do
  echo "Processing ${rel_path}..."
  CDN_URL="https://huggingface.co/datasets/${REPO}/resolve/main/${rel_path}"

  # Download via CDN (no Authorization header)
  tmp=$(mktemp)
  curl -sSf -o "${tmp}" "${CDN_URL}"

  # Lightweight schema projection to {prompt,response} + md5 dedup via lib/dedup.py
  python3 -c "
import sys, json, hashlib, pyarrow as pa, pyarrow.parquet as pq, os
from lib.dedup import DedupStore

dedup = DedupStore()
try:
    table = pq.read_table('${tmp}')
except Exception:
    # fallback: try jsonl
    with open('${tmp}', 'r') as f:
        rows = [json.loads(l) for l in f if l.strip()]
    table = pa.Table.from_pylist(rows)

# Normalize to prompt/response (best-effort)
def normalize(tbl):
    cols = set(tbl.column_names)
    prompt_col = next((c for c in ('prompt','input','question') if c in cols), None)
    response_col = next((c for c in ('response','output','answer') if c in cols), None)
    if prompt_col and response_col:
        return pa.table({'prompt': tbl[prompt_col], 'response': tbl[response_col]})
    # fallback: keep all cols but ensure prompt/response exist
    return tbl

norm = normalize(table)

# Dedup by content hash
for batch in norm.to_batches():
    df = batch.to_pydict()
    n = len(next(iter(df.values()))) if df else 0
    for i in range(n):
        row = {k: df[k][i] for k in df}
        payload = json.dumps(row, sort_keys=True).encode()
        md5 = hashlib.md5(payload).hexdigest()
        if not dedup.seen(md5):
            dedup.add(md5)
            print(json.dumps(row, ensure_ascii=False))
" >> "${OUT_FILE}"

  rm -f "${tmp}"
done

echo "Shard ${SHARD_ID} finished. Output: ${OUT_FILE}"