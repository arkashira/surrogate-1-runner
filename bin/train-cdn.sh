#!/usr/bin/env bash
# train-cdn.sh
# Launch Lightning Studio training with CDN-only file list.
# Reuses running studio when possible to save quota.

set -euo pipefail
export SHELL=/bin/bash

cd "$(dirname "$0")/.."

FILE_LIST="${FILE_LIST:-file-list.json}"
STUDIO_NAME="${STUDIO_NAME:-surrogate-1-train}"
DATE_FOLDER="${DATE_FOLDER:-2026-05-02}"

if [[ ! -f "$FILE_LIST" ]]; then
    echo "Generating file-list for $DATE_FOLDER ..."
    python bin/list-files.py --date "$DATE_FOLDER" --out "$FILE_LIST"
fi

HF_DATASETS_OFFLINE=1 \
lightning studio run \
    --name "$STUDIO_NAME" \
    --script train.py \
    --env "HF_DATASETS_OFFLINE=1" \
    --env "FILE_LIST=$FILE_LIST" \
    --arg "--file-list" "$FILE_LIST" \
    --arg "--cdn"