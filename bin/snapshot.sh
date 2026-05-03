#!/usr/bin/env bash
set -euo pipefail

REPO="${HF_REPO:-axentx/surrogate-1-training-pairs}"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTDIR="${2:-snapshot}"
OUTFILE="${OUTDIR}/${DATE}.json"

mkdir -p "${OUTDIR}"

echo "[snapshot] Listing ${REPO} tree for date ${DATE}..."
files=$(python3 - "$REPO" "$DATE" <<'PY'
import os, json, sys
from huggingface_hub import HfApi
repo_id = sys.argv[1]
date = sys.argv[2]
api = HfApi()
try:
    tree = api.list_repo_tree(repo_id, path=date, recursive=False)
    filenames = sorted(item.path for item in tree if item.path.endswith(".parquet"))
except Exception as e:
    print(json.dumps({"error": str(e)}), file=sys.stderr)
    sys.exit(1)
print(json.dumps(filenames, separators=(",", ":")))
PY
)

if [ -z "${files}" ] || echo "${files}" | grep -q '"error"'; then
    echo "[snapshot] ERROR: Failed to list files for ${DATE}" >&2
    exit 1
fi

# Basic CDN reachability check (first file only, fail fast)
first_file=$(echo "${files}" | jq -r '.[0]')
cdn_url="https://huggingface.co/datasets/${REPO}/resolve/main/${DATE}/${first_file}"
if ! curl -fsSI --retry 2 --max-time 10 "${cdn_url}" > /dev/null 2>&1; then
    echo "[snapshot] ERROR: CDN URL unreachable: ${cdn_url}" >&2
    exit 1
fi

jq -n \
  --arg date "${DATE}" \
  --arg repo "${REPO}" \
  --argjson files "${files}" \
  '{date:$date, repo:$repo, files:$files}' > "${OUTFILE}"

echo "[snapshot] Written ${OUTFILE} with $(jq '.files | length' "${OUTFILE}") files"