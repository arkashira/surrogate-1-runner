#!/usr/bin/env bash
# Usage: HF_TOKEN=... ./preflight-snapshot.sh <date-folder>
# Produces: file-list.json  (array of relative paths under date-folder)
set -euo pipefail

REPO="datasets/axentx/surrogate-1-training-pairs"
DATE_PATH="${1:-$(date +%Y-%m-%d)}"
OUTFILE="file-list.json"

python3 - "$REPO" "$DATE_PATH" "$OUTFILE" <<'PY'
import json, os, sys
from huggingface_hub import HfApi

repo_id, path, out = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi(token=os.environ.get("HF_TOKEN"))
items = api.list_repo_tree(repo_id=repo_id, path=path, recursive=False)
files = [f.rfilename for f in items if f.type == "file"]
with open(out, "w") as fp:
    json.dump(files, fp)
print(f"Snapshot: {len(files)} files -> {out}")
PY