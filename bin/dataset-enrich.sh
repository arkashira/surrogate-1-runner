#!/usr/bin/env bash
set -euo pipefail

SHARD_ID="${SHARD_ID:-0}"
SNAPSHOT="${SNAPSHOT_FILE:-}"

if [[ -n "$SNAPSHOT" && -f "$SNAPSHOT" ]]; then
  echo "Using snapshot $SNAPSHOT for shard $SHARD_ID"
  python3 -c "
import json, sys
from lib.cdn_loader import process_shard
for item in process_shard('$SNAPSHOT', int('$SHARD_ID')):
    print(json.dumps(item, ensure_ascii=False))
"
else
  echo "No snapshot provided, falling back to API list (may hit rate limits)..."
  # existing API-based logic here
fi