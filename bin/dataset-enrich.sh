# Deterministic shard selection (keep existing)
# SHARD_ID=$(( $(echo -n "$slug" | md5sum | tr -d '\n' | od -An -tx1 | head -c8) % 16 ))

if [[ "${SKIP_API_LIST:-0}" == "1" ]]; then
  SNAPSHOT="${SNAPSHOT:-./snapshots/snapshot-$(echo "$REPO" | tr '/-' '__')-${DATE}.json}"
  if [[ ! -f "$SNAPSHOT" ]]; then
    echo "ERROR: SKIP_API_LIST=1 but snapshot not found at $SNAPSHOT" >&2
    exit 1
  fi
  # Build deterministic file list from snapshot
  mapfile -t ALL_FILES < <(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for p in sorted(data['files']):
    print(p)
" "$SNAPSHOT")
else
  # Fallback: runtime listing (existing logic)
  # mapfile -t ALL_FILES < <(python3 -c "... list_repo_tree ...")
  echo "INFO: using runtime HF API listing (SKIP_API_LIST not set)" >&2
  # ... existing listing code ...
fi