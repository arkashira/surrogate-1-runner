#!/usr/bin/env bash
# bin/snapshot.sh
# Generate a snapshot of dataset files for CDN-only ingestion.
# Usage:
#   HF_TOKEN=hf_xxx SNAPSHOT_OUT=snapshots/snapshot-2026-05-02.json \
#     REPO=axentx/surrogate-1-training-pairs \
#     DATE=2026-05-02 \
#     ./bin/snapshot.sh

set -euo pipefail

: "${HF_TOKEN:?required}"
: "${SNAPSHOT_OUT:=snapshot.json}"
: "${REPO:=axentx/surrogate-1-training-pairs}"
: "${DATE:=$(date +%Y-%m-%d)}"

# Ensure snapshots directory exists
mkdir -p "$(dirname "$SNAPSHOT_OUT")"

# Use huggingface_hub to list files non-recursively for the date folder.
python3 - "$REPO" "$DATE" "$SNAPSHOT_OUT" <<'PY'
import os, json, sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

repo_id, date_folder, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi(token=os.environ["HF_TOKEN"])

# List only top-level entries in the date folder (avoids recursive pagination).
entries = api.list_repo_tree(repo_id, path=date_folder, recursive=False)

files = []
for e in entries:
    if getattr(e, "type", None) == "file":
        path = e.path
        # CDN URL (no auth, bypasses /api/ rate limits)
        cdn_url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{path}"
        files.append({
            "path": path,
            "cdn_url": cdn_url,
            "size": getattr(e, "size", None),
            "lfs": getattr(e, "lfs", None) is not None,
        })

snapshot = {
    "repo_id": repo_id,
    "date": date_folder,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "files": files,
    "count": len(files),
}

os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
with open(out_path, "w") as f:
    json.dump(snapshot, f, indent=2)

print(f"Snapshot written: {out_path} ({len(files)} files)")
PY