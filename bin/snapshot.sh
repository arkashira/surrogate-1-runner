#!/usr/bin/env bash
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTDIR="snapshots/${DATE}"
OUTFILE="${OUTDIR}/file-list.json"

mkdir -p "${OUTDIR}"

echo "[$(date -u)] Listing ${REPO} tree for ${DATE} ..."
# Single non-recursive API call per folder (avoids 100x pagination)
# If DATE is a folder prefix, list that folder; else list root.
if curl -s -H "Authorization: Bearer ${HF_TOKEN:-}" \
  "https://huggingface.co/api/datasets/${REPO}/tree?path=${DATE}&recursive=false" \
  | jq -c '.' > "${OUTFILE}.tmp"; then
  mv "${OUTFILE}.tmp" "${OUTFILE}"
  COUNT=$(jq 'length' "${OUTFILE}")
  echo "[$(date -u)] Snapshot saved: ${OUTFILE} (${COUNT} files)"
else
  echo "[$(date-u)] API error or 429 — snapshot failed" >&2
  rm -f "${OUTFILE}.tmp"
  exit 1
fi