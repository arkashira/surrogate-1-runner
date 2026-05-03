#!/usr/bin/env bash
# dataset-enrich.sh
# Usage:
#   # HF datasets mode (existing)
#   HF_TOKEN=... python -m surrogate_1.legacy_worker ...
#
#   # CDN mode (new)
#   CDN_MODE=1 FILE_LIST_JSON=file-list.json python -m surrogate_1.cdn_worker ...

set -euo pipefail
SHELL=/bin/bash

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

export HF_HOME="${HF_HOME:-$REPO_ROOT/.hf_cache}"
mkdir -p "$HF_HOME"

# Dedup store (central)
export DEDUP_DB_PATH="${DEDUP_DB_PATH:-$REPO_ROOT/lib/dedup.db}"

# Mode selection
if [[ "${CDN_MODE:-0}" == "1" && -n "${FILE_LIST_JSON:-}" && -f "$FILE_LIST_JSON" ]]; then
  echo "INFO: CDN mode enabled, file list: $FILE_LIST_JSON"
  exec python -m surrogate_1.cdn_worker --file-list "$FILE_LIST_JSON" "$@"
else
  echo "INFO: HF datasets/legacy mode"
  exec python -m surrogate_1.legacy_worker "$@"
fi