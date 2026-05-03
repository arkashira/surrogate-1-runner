#!/usr/bin/env bash
set -euo pipefail

REPO="${HF_REPO:-axentx/surrogate-1-training-pairs}"
OUTDIR="${1:-manifests}"
DATE="${2:-$(date +%Y-%m-%d)}"

mkdir -p "$OUTDIR/$DATE"

python3 - <<PY
import os, json, sys
from huggingface_hub import HfApi

repo = os.getenv("HF_REPO", "axentx/surrogate-1-training-pairs")
date = os.getenv("DATE", "$DATE")
out = f"$OUTDIR/$DATE/file-list.json"

api = HfApi()
tree = api.list_repo_tree(repo=repo, path=date, recursive=False)
files = [f.rfilename for f in tree if f.type == "file"]

result = {"repo": repo, "date": date, "paths": files}
with open(out, "w") as f:
    json.dump(result, f, indent=2)
print(f"Wrote {len(files)} files to {out}")
PY