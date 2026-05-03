#!/usr/bin/env bash
# bin/make-snapshot.sh
# Usage:
#   HF_TOKEN=hf_xxx REPO=axentx/surrogate-1-training-pairs DATE=2026-05-02 ./bin/make-snapshot.sh
#
# Produces:
#   snapshot/<date>/files.json  (deterministic list of file paths)

set -euo pipefail

: "${HF_TOKEN:?required}"
: "${REPO:?required}"
: "${DATE:?required (YYYY-MM-DD)}"

OUTDIR="snapshot/${DATE}"
OUTFILE="${OUTDIR}/files.json"

mkdir -p "${OUTDIR}"

python3 - <<PY > "${OUTFILE}.tmp"
import os, json, sys
from huggingface_hub import HfApi

api = HfApi(token=os.environ["HF_TOKEN"])
repo = os.environ["REPO"]
date = os.environ["DATE"]

entries = api.list_repo_tree(repo=repo, path=date, recursive=False)

files = []
for e in entries:
    # Keep only files (skip subfolders)
    if getattr(e, "type", None) == "file" or (hasattr(e, "path") and "." in e.path):
        files.append(e.path)

files.sort()
print(json.dumps({"date": date, "files": files}, indent=2))
PY

mv "${OUTFILE}.tmp" "${OUTFILE}"
echo "Snapshot written to ${OUTFILE}"