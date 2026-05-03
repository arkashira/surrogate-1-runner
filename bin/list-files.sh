#!/usr/bin/env bash
# list-files.sh
# Usage: HF_TOKEN=<token> ./list-files.sh <repo> <date_folder> [out.json]
# Example: HF_TOKEN=$HF_TOKEN ./list-files.sh axentx/surrogate-1-training-pairs 2026-05-02 file-list.json

set -euo pipefail

REPO="${1:?repo required}"
DATE_FOLDER="${2:?date_folder required}"
OUT="${3:-file-list.json}"

python3 - <<PY
import os, json, hashlib, sys
from huggingface_hub import HfApi

api = HfApi(token=os.environ.get("HF_TOKEN"))
repo = "$REPO"
folder = "$DATE_FOLDER"

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

records = []
to_walk = [folder.rstrip("/")]
while to_walk:
    current = to_walk.pop(0)
    try:
        items = api.list_repo_tree(repo=repo, path=current, repo_type="dataset")
    except Exception as e:
        print(f"Error listing {current}: {e}", file=sys.stderr)
        sys.exit(1)
    for item in items:
        rfn = item.rfilename
        if rfn.endswith("/"):
            to_walk.append(rfn)
        else:
            # Fetch minimal metadata (size) via repo/file metadata when available.
            # list_repo_tree may include size; if not, we leave size null.
            size = getattr(item, 'size', None)
            records.append({
                "path": rfn,
                "size": size,
                "sha256": None  # will be filled on download if needed
            })

with open("$OUT", "w") as f:
    json.dump({"repo": repo, "date_folder": folder, "files": sorted(records, key=lambda x: x["path"])}, f, indent=2)
print(f"Wrote {len(records)} files to $OUT")
PY