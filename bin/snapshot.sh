#!/usr/bin/env bash
# bin/snapshot.sh
# Generate a deterministic file-list snapshot for a date folder.
# Usage: HF_TOKEN=... ./bin/snapshot.sh <repo> <date_folder> [out.json]
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE_FOLDER="${2:-$(date +%Y-%m-%d)}"
OUT="${3:-snapshot-${DATE_FOLDER}.json}"

python3 - "$REPO" "$DATE_FOLDER" "$OUT" <<'PY'
import os, json, sys
from huggingface_hub import HfApi

repo, date_folder, out = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi(token=os.environ.get("HF_TOKEN"))

# Non-recursive to avoid pagination explosion
tree = api.list_repo_tree(repo=repo, path=date_folder, recursive=False)
files = [item.rfilename for item in tree if item.rfilename.endswith((".parquet", ".jsonl", ".csv"))]
files.sort()

manifest = {"repo": repo, "date_folder": date_folder, "files": files}
with open(out, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Snapshot: {len(files)} files -> {out}")
PY

echo "Snapshot written to $OUT"