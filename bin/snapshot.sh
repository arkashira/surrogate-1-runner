#!/usr/bin/env bash
# bin/snapshot.sh
# Generate a file manifest for a dataset repo/date folder to enable CDN-only downloads.
# Usage:
#   HF_TOKEN=... ./bin/snapshot.sh \
#     --repo axentx/surrogate-1-training-pairs \
#     --path batches/public-merged/2026-05-02 \
#     --out snapshot/2026-05-02/files.json

set -euo pipefail

REPO=""
PATH_PREFIX=""
OUT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --repo) REPO="$2"; shift 2 ;;
    --path) PATH_PREFIX="$2"; shift 2 ;;
    --out)  OUT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$REPO" || -z "$PATH_PREFIX" || -z "$OUT" ]]; then
  echo "Usage: $0 --repo <owner/repo> --path <folder> --out <file.json>"
  exit 1
fi

mkdir -p "$(dirname "$OUT")"

python3 - <<PY
import json
import os
from huggingface_hub import HfApi

api = HfApi(token=os.getenv("HF_TOKEN"))
repo = "${REPO}"
path_prefix = "${PATH_PREFIX}"
out_path = "${OUT}"

def list_files_recursive(api, repo, root):
    files = []
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = api.list_repo_tree(repo=repo, path=current, recursive=False)
        except Exception as ex:
            print(f"Warning: could not list {current}: {ex}")
            continue
        for e in entries:
            if e.type == "file":
                files.append({
                    "path": e.path,
                    "cdn_url": f"https://huggingface.co/datasets/{repo}/resolve/main/{e.path}",
                    "size": getattr(e, "size", None),
                    "sha": getattr(e, "sha", None)
                })
            elif e.type == "folder":
                stack.append(e.path)
    return files

files = list_files_recursive(api, repo, path_prefix)
files.sort(key=lambda x: x["path"])

with open(out_path, "w") as f:
    json.dump({"repo": repo, "path_prefix": path_prefix, "files": files}, f, indent=2)

print(f"Wrote {len(files)} files to {out_path}")
PY