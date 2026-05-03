#!/usr/bin/env bash
# bin/snapshot.sh
# Generate deterministic snapshot.json for a date folder in axentx/surrogate-1-training-pairs
# Usage: SNAPSHOT_DATE=2026-04-29 ./bin/snapshot.sh > snapshot.json

set -euo pipefail

REPO="${HF_REPO:-axentx/surrogate-1-training-pairs}"
DATE="${SNAPSHOT_DATE:-$(date +%Y-%m-%d)}"
HF_TOKEN="${HF_TOKEN:-}"

# Single API call: list top-level objects in the date folder (non-recursive by default)
# We'll recurse client-side only for that date subtree to avoid 100x pagination.
# Use huggingface_hub via python for reliable tree listing.
python3 - "$REPO" "$DATE" "$HF_TOKEN" <<'PY'
import os
import json
import sys
from huggingface_hub import HfApi

repo = sys.argv[1]
date = sys.argv[2]
token = sys.argv[3] or None

api = HfApi(token=token)
# recursive=True limited to the date subtree only
items = api.list_repo_tree(repo=repo, path=date, recursive=True)

snapshot = {
    "repo": repo,
    "date": date,
    "generated_at_utc": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "files": []
}

for item in sorted(items, key=lambda x: x.path):
    if item.type != "file":
        continue
    # CDN URL (no auth, bypasses API rate limits)
    cdn_url = f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
    snapshot["files"].append({
        "path": item.path,
        "cdn_url": cdn_url,
        "size": getattr(item, "size", None),
        "lfs": getattr(item, "lfs", None) is not None
    })

json.dump(snapshot, sys.stdout, indent=2)
PY