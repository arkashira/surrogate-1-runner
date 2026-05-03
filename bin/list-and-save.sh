#!/usr/bin/env bash
# Usage: HF_TOKEN=... ./bin/list-and-save.sh <date-folder> [output.json]
# Example: ./bin/list-and-save.sh 2026-05-03 file-list-2026-05-03.json
set -euo pipefail

REPO="${HF_REPO_BASE:-datasets/axentx/surrogate-1-training-pairs}"
DATE_PATH="${1:-}"
OUT="${2:-file-list.json}"

if [[ -z "$DATE_PATH" ]]; then
  echo "Usage: $0 <date-folder> [output.json]"
  exit 1
fi

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "HF_TOKEN required for list_repo_tree (one-time bootstrap)"
  exit 1
fi

python3 - "$REPO" "$DATE_PATH" "$OUT" <<'PY'
import os, json, sys
from huggingface_hub import HfApi

repo_id, date_path = sys.argv[1], sys.argv[2]
out_path = sys.argv[3]

api = HfApi(token=os.environ["HF_TOKEN"])
# Non-recursive: list immediate children in the date folder
tree = api.list_repo_tree(repo_id=repo_id, path=date_path, recursive=False)

files = []
for item in tree:
    # item.path is like "2026-05-03/somefile.parquet"
    if not item.path.endswith("/"):  # skip subfolders
        files.append(item.path)

with open(out_path, "w") as f:
    json.dump({"date": date_path, "files": sorted(files)}, f, indent=2)

print(f"Saved {len(files)} files to {out_path}")
PY