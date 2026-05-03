#!/usr/bin/env bash
# bin/list-date-folder.sh
# Usage: ./list-date-folder.sh 2026-05-03 > file-list-2026-05-03.json
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE_FOLDER="${2:-$(date +%Y-%m-%d)}"
HF_TOKEN="${HF_TOKEN:-}"

URL="https://huggingface.co/api/datasets/${REPO}/tree?path=${DATE_FOLDER}&recursive=false"

if [[ -n "$HF_TOKEN" ]]; then
  curl -sL -H "Authorization: Bearer ${HF_TOKEN}" "$URL"
else
  curl -sL "$URL"
fi