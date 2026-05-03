#!/usr/bin/env bash
# bin/snapshot.sh
# Generate a file manifest for a date folder in axentx/surrogate-1-training-pairs
# Usage: bin/snapshot.sh <date> [output.json]
# Example: bin/snapshot.sh 2026-05-02

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="${2:-snapshot-${DATE}.json}"

echo "Listing dataset tree for ${REPO}/batches/public-merged/${DATE} ..."

python3 - <<PY
import json, os, sys
from huggingface_hub import HfApi

repo = os.environ.get("REPO", "$REPO")
date = os.environ.get("DATE", "$DATE")
out = os.environ.get("OUT", "$OUT")

api = HfApi()
# non-recursive listing of the date folder
tree = api.list_repo_tree(
    repo=repo,
    path=f"batches/public-merged/{date}",
    recursive=False,
)

files = []
for item in tree:
    if item.type != "file":
        continue
    # CDN URL (no auth)
    cdn = f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
    files.append({
        "path": item.path,
        "cdn_url": cdn,
        "size": getattr(item, "size", None),
    })

os.makedirs(os.path.dirname(out) if os.path.dirname(out) else ".", exist_ok=True)
with open(out, "w") as f:
    json.dump({"date": date, "files": files}, f, indent=2)

print(f"Wrote {len(files)} files to {out}")
PY

echo "Snapshot saved to ${OUT}"