#!/usr/bin/env bash
# bin/list-date-folder.sh
# Usage: HF_TOKEN=... ./bin/list-date-folder.sh <date-folder> > file-list-<date>.json
set -euo pipefail

REPO="datasets/axentx/surrogate-1-training-pairs"
FOLDER="${1:-}"
if [[ -z "$FOLDER" ]]; then
  echo "Usage: $0 <date-folder>" >&2
  exit 1
fi

python3 - <<PY
import os, json, sys
from huggingface_hub import HfApi

api = HfApi(token=os.environ.get("HF_TOKEN"))
repo = os.environ.get("REPO", "$REPO")
folder = os.environ.get("FOLDER", "$FOLDER")

tree = api.list_repo_tree(repo=repo, path=folder, recursive=False)
files = [item.rfilename for item in tree if item.type == "file"]
sys.stdout.write(json.dumps(files))
PY