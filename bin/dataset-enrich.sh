# Near top, after shebang and set -euo pipefail
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"

# If snapshot provided, use CDN-only mode
if [[ -n "$SNAPSHOT_FILE" && -f "$SNAPSHOT_FILE" ]]; then
  echo "Using snapshot $SNAPSHOT_FILE (CDN mode)"
  # Select shard slice from snapshot entries
  mapfile -t ALL_URLS < <(jq -r '.[].cdn_url' "$SNAPSHOT_FILE")
  TOTAL=${#ALL_URLS[@]}
  SHARD_SIZE=$(( (TOTAL + SHARDS - 1) / SHARDS ))
  START=$(( SHARD_ID * SHARD_SIZE ))
  END=$(( START + SHARD_SIZE ))
  if (( END > TOTAL )); then END=$TOTAL; fi
  SHARD_URLS=("${ALL_URLS[@]:$START:$((END-START))}")
  echo "Shard $SHARD_ID: ${#SHARD_URLS[@]}/${TOTAL} URLs"
else
  # Fallback to original HF API listing (keep existing behavior)
  echo "No snapshot provided — using HF API listing (rate-limited)"
  # ... existing list_repo_tree logic ...
fi

# Later, where you stream/process files:
# Replace `load_dataset(streaming=True)` usage with:
python3 -c "
import sys, json
sys.path.insert(0, 'lib')
from cdn_stream import iter_cdn_shard
urls = json.loads('$(printf '%s\n' "${SHARD_URLS[@]}" | jq -R . | jq -s .)')
for row in iter_cdn_shard(urls, columns=('prompt','response')):
    # apply per-schema normalization + dedup via lib/dedup.py
    print(json.dumps(row))
" | ...