#!/usr/bin/env bash
# ... existing header ...

# If a snapshot is provided, use it to get the deterministic file list.
if [[ -n "${SNAPSHOT_FILE:-}" && -f "$SNAPSHOT_FILE" ]]; then
  echo "Using snapshot: $SNAPSHOT_FILE"
  mapfile -t ALL_FILES < <(python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['files']))" "$SNAPSHOT_FILE")
else
  echo "WARNING: No snapshot provided; falling back to live API (may hit rate limits)."
  # Existing logic to list files (keep as fallback)
  mapfile -t ALL_FILES < <(python3 - "$REPO" <<'PY'
import os, sys
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get("HF_TOKEN"))
repo = sys.argv[1]
# Simplified: list top-level non-recursive; adapt as needed
tree = api.list_repo_tree(repo=repo, path="", recursive=True)
files = [item.rfilename for item in tree if item.rfilename.endswith((".parquet",".jsonl",".csv"))]
files.sort()
print("\n".join(files))
PY
  )
fi

TOTAL=${#ALL_FILES[@]}
if (( TOTAL == 0 )); then
  echo "No files found. Exiting."
  exit 0
fi

# Deterministic shard slice (same as before)
SHARD_FILES=()
for i in "${!ALL_FILES[@]}"; do
  if (( i % 16 == SHARD_ID )); then
    SHARD_FILES+=("${ALL_FILES[$i]}")
  fi
done

echo "Shard $SHARD_ID processing ${#SHARD_FILES[@]}/$TOTAL files"

# Download via CDN (no auth header) and process
for rel_path in "${SHARD_FILES[@]}"; do
  url="https://huggingface.co/datasets/${REPO}/resolve/main/${rel_path}"
  tmp=$(mktemp)
  if curl -fsSL "$url" -o "$tmp"; then
    # Existing normalize/dedup/upload logic here
    # ...
    echo "Processed $rel_path"
  else
    echo "Failed to download $url"
  fi
  rm -f "$tmp"
done