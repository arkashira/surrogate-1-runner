#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Accepts snapshot file as first arg; falls back to API if missing.

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
SHARD_ID="${SHARD_ID:-0}"
SNAPSHOT="${1:-snapshot.json}"

source "$(dirname "$0")/lib/dedup.py"  # if needed for md5 store

if [[ -f "$SNAPSHOT" ]]; then
  echo "Using snapshot $SNAPSHOT"
  mapfile -t FILES < <(python3 -c "
import sys, json
from lib.snapshot import files_for_shard
snapshot = json.load(open('$SNAPSHOT'))
for f in files_for_shard(snapshot, $SHARD_ID):
    print(f['path'])
")
else
  echo "Snapshot not found, falling back to API (may hit rate limits)..."
  # fallback: use huggingface_hub to list files (existing behavior)
  mapfile -t FILES < <(python3 -c "
from huggingface_hub import list_repo_files
for f in list_repo_files('$REPO'):
    print(f)
")
fi

for relpath in "${FILES[@]}"; do
  url="https://huggingface.co/datasets/$REPO/resolve/main/$relpath"
  echo "Processing $relpath via CDN: $url"
  # Download via CDN (no auth), project to {prompt,response}, dedup, append to shard output
  curl -sSL "$url" -o "/tmp/$(basename "$relpath")"
  # ... existing normalization logic ...
done