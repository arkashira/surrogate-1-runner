#!/usr/bin/env bash
# bin/list-folder.sh
# Usage: HF_TOKEN=... ./bin/list-folder.sh <repo> <date-folder> > file-list.json
# Example: ./bin/list-folder.sh axentx/surrogate-1-training-pairs batches/public-merged/2026-05-02

set -euo pipefail
REPO="${1:-axentx/surrogate-1-training-pairs}"
FOLDER="${2:-}"

if [ -z "$FOLDER" ]; then
  echo "Usage: $0 <repo> <folder>" >&2
  exit 1
fi

python3 - "$REPO" "$FOLDER" <<'PY'
import json, os, sys
from huggingface_hub import HfApi

repo_id = sys.argv[1]
folder = sys.argv[2].rstrip("/")
api = HfApi(token=os.environ.get("HF_TOKEN"))
# non-recursive: one API call, no pagination explosion
items = api.list_repo_tree(repo_id, path=folder, recursive=False)
files = [it.rfilename for it in items if not it.rfilename.endswith("/")]
print(json.dumps({"repo": repo_id, "folder": folder, "files": files}, indent=2))
PY