#!/usr/bin/env bash
set -euo pipefail

# Usage: bin/snapshot.sh [YYYY-MM-DD]
# Requires: huggingface_hub (pip), HF_TOKEN (read-only is fine for public repos)
# Emits: snapshots/<DATE>.json

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTDIR="snapshots"
OUTFILE="${OUTDIR}/${DATE}.json"

mkdir -p "${OUTDIR}"

python3 - <<PY
import os, json, sys
from huggingface_hub import HfApi

repo = os.environ.get("REPO", "${REPO}")
date = "${DATE}"
path = f"public-merged/{date}"
api = HfApi()

try:
    # Single API call: recursive tree listing for the date folder
    tree = api.list_repo_tree(repo=repo, path=path, recursive=True)
except Exception as e:
    print(f"ERROR listing repo tree: {e}", file=sys.stderr)
    sys.exit(1)

files = []
for item in tree:
    if item.type != "file":
        continue
    # Only include .jsonl and .parquet files
    if not (item.path.endswith(".jsonl") or item.path.endswith(".parquet")):
        continue
    # CDN URL (no Authorization header required)
    cdn = f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
    files.append({
        "path": item.path,
        "cdn": cdn,
        "size": getattr(item, "size", None)
    })

out = os.path.join(os.environ.get("OUTDIR", "${OUTDIR}"), "${DATE}.json")
with open(out, "w") as f:
    json.dump({"date": date, "root": path, "files": files}, f, indent=2)

print(f"Wrote {len(files)} files to {out}")
PY

echo "Snapshot created: ${OUTFILE}"