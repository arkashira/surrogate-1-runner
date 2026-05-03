#!/usr/bin/env bash
set -euo pipefail

REPO=${HF_REPO:-"axentx/surrogate-1-training-pairs"}
DATE=${1:-$(date +%Y-%m-%d)}
OUTDIR="./snapshots"
OUTFILE="${OUTDIR}/${DATE}.json"

mkdir -p "${OUTDIR}"

python3 - <<PY
import os, json, hashlib
from huggingface_hub import HfApi

api = HfApi()
repo = os.environ["HF_REPO"]
date = os.environ["DATE"]
folder = f"batches/public-merged/{date}"

try:
    tree = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    files = [f.rfilename for f in tree if f.rfilename.endswith(".parquet")]
except Exception as e:
    # If folder missing, treat as empty
    files = []

files.sort()
payload = {
    "date": date,
    "folder": folder,
    "files": files,
    "sha256": hashlib.sha256(json.dumps(files).encode()).hexdigest()
}

with open(os.environ["OUTFILE"], "w") as f:
    json.dump(payload, f, indent=2)

print(f"Snapshot {date}: {len(files)} files -> {os.environ['OUTFILE']}")
PY