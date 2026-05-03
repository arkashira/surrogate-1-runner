#!/usr/bin/env bash
# Generate a snapshot of dataset files for CDN-only ingestion.
# Usage: HF_TOKEN=... HF_REPO=... ./snapshot.sh [output-dir]
set -euo pipefail

REPO="${HF_REPO:-datasets/axentx/surrogate-1-training-pairs}"
OUTDIR="${1:-snapshot}"
DATE_PART=$(date +%Y-%m-%d)
OUTFILE="${OUTDIR}/${DATE_PART}/files.json"

mkdir -p "$(dirname "$OUTFILE")"

echo "Generating snapshot for ${REPO}..."
HF_REPO="${REPO}" OUT="${OUTFILE}" python3 bin/generate-file-list.py

# Produce a compact manifest for training (just paths + cdn urls)
jq -c '.[] | {path, cdn_url}' "${OUTFILE}" > "${OUTDIR}/${DATE_PART}/manifest.ndjson"

echo "Snapshot saved to ${OUTFILE}"
echo "Manifest saved to ${OUTDIR}/${DATE_PART}/manifest.ndjson"