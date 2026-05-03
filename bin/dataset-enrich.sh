#!/usr/bin/env bash
# Usage: HF_TOKEN=... SHARD_ID=0 ./dataset-enrich.sh <date-folder>
set -euo pipefail

REPO="datasets/axentx/surrogate-1-training-pairs"
DATE_PATH="${1:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"
N_SHARDS="${N_SHARDS:-16}"
TS=$(date +%H%M%S)
OUTDIR="batches/public-merged/${DATE_PATH}"
OUTFILE="${OUTDIR}/shard${SHARD_ID}-${TS}.jsonl"
FILE_LIST="file-list.json"

mkdir -p "$OUTDIR"

# Deterministic shard assignment by filename hash
should_process() {
  local slug="$1"
  local hash=$(( $(echo -n "$slug" | cksum | cut -d' ' -f1) % N_SHARDS ))
  [[ $hash -eq $SHARD_ID ]]
}

# Project raw file to {prompt,response}
project_pair() {
  local file="$1"
  python3 - "$file" <<'PY'
import json, sys, os
try:
    with open(sys.argv[1]) as f:
        data = json.load(f)
except Exception:
    print(json.dumps({"prompt": open(sys.argv[1]).read().strip(), "response": ""}))
    sys.exit(0)

prompt = data.get("prompt") or data.get("input") or data.get("question") or ""
response = data.get("response") or data.get("output") or data.get("answer") or ""
if isinstance(prompt, (dict, list)):
    prompt = json.dumps(prompt)
if isinstance(response, (dict, list)):
    response = json.dumps(response)
print(json.dumps({"prompt": str(prompt).strip(), "response": str(response).strip()}))
PY
}

# Download via CDN and project
process_file() {
  local rel_path="$1"
  local tmp
  tmp=$(mktemp)
  if curl -fsSL "https://huggingface.co/${REPO}/resolve/main/${rel_path}" -o "$tmp"; then
    project_pair "$tmp"
    rm -f "$tmp"
  else
    echo "WARN: failed to fetch ${rel_path}" >&2
    rm -f "$tmp"
    return 1
  fi
}

if [[ ! -f "$FILE_LIST" ]]; then
  echo "ERROR: ${FILE_LIST} not found. Run bin/preflight-snapshot.sh first." >&2
  exit 1
fi

mapfile -t FILES < <(python3 -c "import json,sys; files=json.load(open(sys.argv[1])); print('\n'.join(files))" "$FILE_LIST")

count=0
for rel_path in "${FILES[@]}"; do
  if ! should_process "$rel_path"; then
    continue
  fi
  pair=$(process_file "$rel_path") || continue
  if python3 lib/dedup.py --check-and-add <<<"$pair"; then
    echo "$pair" >> "$OUTFILE"
    ((count++)) || true
  fi
done

echo "Shard ${SHARD_ID}: wrote ${count} pairs to ${OUTFILE}"