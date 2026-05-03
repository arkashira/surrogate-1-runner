#!/usr/bin/env bash
set -euo pipefail

# Usage: make-snapshot.sh <date-folder> [output.json]
# Example: make-snapshot.sh public-merged/2026-05-02 snapshot/2026-05-02.json

REPO="axentx/surrogate-1-training-pairs"
FOLDER="${1:-public-merged/$(date +%Y-%m-%d)}"
OUT="${2:-snapshot/$(basename "$FOLDER").json}"

mkdir -p "$(dirname "$OUT")"

python3 - "$REPO" "$FOLDER" "$OUT" <<'PY'
import json, os, sys
from datetime import datetime
from huggingface_hub import HfApi

repo_id, folder, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi()

tree = api.list_repo_tree(repo_id=repo_id, path=folder, recursive=False)
files = sorted(item.rfilename for item in tree if item.type == "file")

if not files:
    sys.exit(f"No files found in {repo_id}/{folder}")

snapshot = {
    "repo": repo_id,
    "folder": folder,
    "date": os.path.basename(folder.rstrip("/")),
    "files": files,
    "created_at": datetime.utcnow().isoformat() + "Z"
}

with open(out_path, "w") as f:
    json.dump(snapshot, f, indent=2)
print(f"Snapshot written to {out_path} ({len(files)} files)")
PY