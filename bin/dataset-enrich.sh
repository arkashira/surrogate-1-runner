#!/usr/bin/env bash
set -euo pipefail
# If SNAPSHOT_FILE is provided, use it; otherwise fall back to live listing.

SHARD_ID="${SHARD_ID:?required}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"

if [[ -n "$SNAPSHOT_FILE" && -f "$SNAPSHOT_FILE" ]]; then
  echo "Using snapshot $SNAPSHOT_FILE for shard $SHARD_ID"
  python3 -c "
import sys, json
from lib.file_list import shard_files
for f in shard_files('$SNAPSHOT_FILE', int('$SHARD_ID')):
    print(f['remote_path'])
" | while read -r remote_path; do
    # Process each file (streaming, project to {prompt,response} only)
    process_one_file "$remote_path"
  done
else
  echo "No snapshot; falling back to live listing (may hit rate limits)"
  # existing logic using huggingface_hub list_repo_files...
fi