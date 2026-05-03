#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Existing behavior preserved; new optional arg --file-list FILELIST

set -euo pipefail

# ... existing env setup ...

FILE_LIST=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --file-list) FILE_LIST="$2"; shift 2 ;;
    *) break ;;
  esac
done

# Pass FILE_LIST into python worker via env
export SURROGATE_FILE_LIST="${FILE_LIST}"
exec python3 -m surrogate_1.worker "$@"