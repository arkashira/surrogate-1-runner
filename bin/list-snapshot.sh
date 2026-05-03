#!/usr/bin/env bash
# Generate deterministic snapshot for today's folder.
# Usage: HF_TOKEN=... ./bin/list-snapshot.sh > snapshot.json
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE=$(date -u +%Y-%m-%d)
FOLDER="public-raw/${DATE}"  # adjust if your layout differs

# list single-level tree for the date folder (non-recursive)
python3 - "$REPO" "$FOLDER" <<'PY'
import os, json, sys
from huggingface_hub import HfApi

repo = sys.argv[1]
folder = sys.argv[2].rstrip("/")
api = HfApi(token=os.environ.get("HF_TOKEN"))
entries = api.list_repo_tree(repo=repo, path=folder, recursive=False)

out = []
for e in entries:
    if e.type != "file":
        continue
    # CDN URL bypasses API auth/rate limits
    cdn = f"https://huggingface.co/datasets/{repo}/resolve/main/{e.path}"
    out.append({"path": e.path, "cdn": cdn, "size": e.size})

sys.stdout.write(json.dumps({"date": folder, "entries": out}, indent=2))
PY