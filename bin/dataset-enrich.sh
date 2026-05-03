# Near top of bin/dataset-enrich.sh (after shebang and set -euo pipefail)

# Optional: generate pre-flight snapshot for this date folder.
# Controlled by env var to avoid extra API calls when not wanted.
if [[ "${SNAPSHOT:-false}" == "true" ]]; then
  DATE_FOLDER="${DATE_FOLDER:-$(date -u +%Y-%m-%d)}"
  SHARD_ID="${SHARD_ID:-0}"
  SNAPSHOT_OUT="${SNAPSHOT_OUT:-./snapshots/${DATE_FOLDER}-shard${SHARD_ID}.json}"
  echo "Generating snapshot for ${DATE_FOLDER} -> ${SNAPSHOT_OUT}"
  ./bin/snapshot.sh --repo axentx/surrogate-1-training-pairs \
    --date "$DATE_FOLDER" \
    --out "$SNAPSHOT_OUT" || echo "Snapshot failed (non-fatal)"
fi

# Optional: if SNAPSHOT_FILE is provided, skip live list_repo_tree and use manifest.
if [[ -n "${SNAPSHOT_FILE:-}" ]]; then
  if [[ ! -f "$SNAPSHOT_FILE" ]]; then
    echo "ERROR: SNAPSHOT_FILE not found: $SNAPSHOT_FILE" >&2
    exit 1
  fi
  # Validate snapshot contains expected date prefix to avoid mixing folders.
  DATE_PREFIX=$(jq -r '.date' "$SNAPSHOT_FILE" 2>/dev/null || true)
  if [[ -z "$DATE_PREFIX" || "$DATE_PREFIX" != "$DATE_FOLDER"* ]]; then
    echo "ERROR: SNAPSHOT_FILE date mismatch (expected ${DATE_PREFIX:-none} to match ${DATE_FOLDER})" >&2
    exit 1
  fi
  echo "Using snapshot file: $SNAPSHOT_FILE"
  # Replace live listing with manifest-driven file list.
  # (Keep existing per-file streaming/download logic unchanged.)
fi