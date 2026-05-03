#!/usr/bin/env bash
# bin/list-snapshot.sh
# Usage: HF_TOKEN=... ./bin/list-snapshot.sh axentx/surrogate-1-training-pairs 2026-05-02 > snapshot-2026-05-02.json
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE="${2:-$(date +%F)}"
FOLDER="public-raw/${DATE}"

python3 - "$REPO" "$FOLDER" <<'PY'
import os, json, sys
from huggingface_hub import HfApi

repo_id = sys.argv[1]
folder = sys.argv[2].rstrip("/")
api = HfApi(token=os.environ.get("HF_TOKEN"))

# Single API call: non-recursive per folder to avoid pagination explosion.
entries = api.list_repo_tree(repo_id, path=folder, recursive=False)

files = []
for e in entries:
    if not e.path.endswith((".jsonl", ".parquet", ".json")):
        continue
    files.append({
        "path": e.path,
        "cdn_url": f"https://huggingface.co/datasets/{repo_id}/resolve/main/{e.path}"
    })

sys.stdout.write(json.dumps({"repo": repo_id, "folder": folder, "files": files}, indent=2))
PY