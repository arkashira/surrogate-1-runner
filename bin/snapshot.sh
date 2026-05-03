#!/usr/bin/env bash
# Generate snapshot of dataset files for a date folder.
# Usage: SNAPSHOT_DATE=2026-05-02 ./bin/snapshot.sh
# Outputs: snapshot/latest.json and snapshot/<date>.json
set -euo pipefail

REPO="${HF_DATASET_REPO:-axentx/surrogate-1-training-pairs}"
DATE_FOLDER="${SNAPSHOT_DATE:-$(date -u +%Y-%m-%d)}"
OUT_DIR="snapshot"
LATEST="${OUT_DIR}/latest.json"
DATED="${OUT_DIR}/${DATE_FOLDER}.json"

mkdir -p "${OUT_DIR}"

echo "Generating snapshot for ${REPO} -> public-merged/${DATE_FOLDER}"
python3 bin/lib/snapshot.py "${REPO}" "public-merged/${DATE_FOLDER}" "${DATED}"

# Also keep latest
cp "${DATED}" "${LATEST}"

echo "Snapshot saved: ${DATED}"
echo "Files: $(jq '.count' "${DATED}")"