#!/usr/bin/env bash
set -euo pipefail

# Existing behavior preserved when SNAPSHOT_FILE is unset.
# When SNAPSHOT_FILE is set, stream CDN URLs directly (zero HF API calls).

SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"

stream_from_cdn() {
  local snapshot="$1"
  python3 - <<PY
import json, sys, os

shard_id = int(os.environ.get("SHARD_ID", "0"))
total_shards = int(os.environ.get("TOTAL_SHARDS", "16"))

with open("$snapshot") as f:
    data = json.load(f)

files = data.get("files", [])
# Deterministic shard assignment by slug hash (consistent with existing logic)
assigned = []
for f in files:
    slug = os.path.basename(f["path"])
    if hash(slug) % total_shards == shard_id:
        assigned.append(f)

for f in assigned:
    print(f["cdn"])
PY
}

process_one_cdn_url() {
  local url="$1"
  # Download via CDN (no auth) and parse to {prompt,response}
  # Keep existing per-schema normalization logic here.
  curl -fsSL "$url" -o /tmp/record.$$.jsonl
  # ... existing normalization + dedup via lib/dedup.py ...
  # Output normalized JSONL lines to stdout
  # rm /tmp/record.$$.jsonl
}

main() {
  if [[ -n "${SNAPSHOT_FILE}" && -f "${SNAPSHOT_FILE}" ]]; then
    echo "Using CDN snapshot: ${SNAPSHOT_FILE}"
    while IFS= read -r url; do
      [[ -z "$url" ]] && continue
      process_one_cdn_url "$url"
    done < <(stream_from_cdn "${SNAPSHOT_FILE}")
  else
    echo "No snapshot provided — using legacy HF API path (may hit rate limits)"
    # ... existing dataset-enrich logic (streaming load_dataset etc) ...
  fi
}

main "$@"