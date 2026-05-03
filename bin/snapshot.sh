#!/usr/bin/env bash
# bin/snapshot.sh
# Generate a CDN file manifest for a date folder to avoid HF API calls during training.
#
# Usage:
#   HF_DATASET_REPO=datasets/axentx/surrogate-1-training-pairs \
#     bin/snapshot.sh <date-folder> [out-dir]
#
# Examples:
#   bin/snapshot.sh 2026-04-29
#   bin/snapshot.sh public-merged/2026-04-29 ./manifests
#
# Exit codes:
#   0 - success (manifest written)
#   1 - invalid args or API error (including 429)

set -euo pipefail
export SHELL=/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DATE_FOLDER="${1:-}"
if [[ -z "$DATE_FOLDER" ]]; then
  echo "ERROR: date-folder is required" >&2
  echo "Usage: $0 <date-folder> [out-dir]" >&2
  exit 1
fi

OUT_DIR="${2:-${REPO_ROOT}/batches/public-merged}"
HF_DATASET_REPO="${HF_DATASET_REPO:-datasets/axentx/surrogate-1-training-pairs}"

export HF_DATASET_REPO

cd "$REPO_ROOT"
if ! python3 "${REPO_ROOT}/lib/snapshot.py" "$DATE_FOLDER" "$OUT_DIR"; then
  echo "ERROR: failed to generate snapshot (possible HF API 429)" >&2
  exit 1
fi