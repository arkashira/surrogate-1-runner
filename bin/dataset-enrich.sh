#!/usr/bin/env bash
# bin/dataset-enrich.sh
# Usage: FILELIST=path/to/snapshot.json ./bin/dataset-enrich.sh
set -euo pipefail

FILELIST="${FILELIST:-}"
if [[ -n "$FILELIST" && -f "$FILELIST" ]]; then
  echo "Using filelist: $FILELIST"
  mapfile -t TARGET_FILES < <(jq -r '.files[]' "$FILELIST")
else
  echo "WARNING: No filelist provided; listing repo tree (may hit API limits)" >&2
  # fallback to existing behavior
fi

# Add retry/backoff for CDN downloads
download_with_retry() {
  local url="$1" outfile="$2" max_retries=3 backoff=1
  for i in $(seq 1 "$max_retries"); do
    if curl -f -s -o "$outfile" "$url"; then
      return 0
    fi
    echo "Download failed (attempt $i/$max_retries): $url" >&2
    sleep "$backoff"
    backoff=$((backoff * 2))
  done
  echo "Failed to download after $max_retries attempts: $url" >&2
  return 1
}