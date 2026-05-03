#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... ./bin/snapshot.sh axentx/surrogate-1-training-pairs 2026-05-03
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE="${2:-$(date +%Y-%m-%d)}"
OUTDIR="snapshots/${DATE}"
MANIFEST="${OUTDIR}/snapshot.json"

mkdir -p "${OUTDIR}"

echo "Listing ${REPO} tree for date=${DATE} ..."
# Single API call; recursive=False to avoid pagination explosion
python3 - <<PY > "${OUTDIR}/tree.json"
import os, json, sys
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get("HF_TOKEN"))
repo = sys.argv[1]
date = sys.argv[2]
items = api.list_repo_tree(repo, path=date, recursive=False)
# Keep only files (exclude subfolders)
files = [it for it in items if it.type == "file"]
print(json.dumps([{"path": f.path, "size": getattr(f, "size", None)} for f in files], indent=2))
PY "$REPO" "$DATE"

echo "Building manifest with CDN URLs ..."
python3 bin/build_manifest.py "${OUTDIR}/tree.json" "$REPO" "$DATE" > "$MANIFEST"
echo "Snapshot written to $MANIFEST"