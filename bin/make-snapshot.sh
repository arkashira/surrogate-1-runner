#!/usr/bin/env bash
# Generate deterministic snapshot for a date folder.
# Usage:
#   HF_TOKEN=<token> ./make-snapshot.sh 2026-05-01 ./snapshots/file-list-2026-05-01-$(date +%H%M%S).json

set -euo pipefail

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "ERROR: HF_TOKEN is required" >&2
  exit 1
fi

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <date_folder> <output.json>" >&2
  exit 1
fi

DATE_FOLDER=$1
OUT=$2

export HUGGING_FACE_HUB_TOKEN="$HF_TOKEN"

mkdir -p "$(dirname "$OUT")"

python3 tools/snapshot.py "$DATE_FOLDER" "$OUT"