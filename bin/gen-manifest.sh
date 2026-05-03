#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE="${2:-$(date +%Y-%m-%d)}"
OUT="${3:-manifest-${DATE}.json}"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json, os, sys
from huggingface_hub import HfApi

repo_id, date_folder, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi()

# One non-recursive tree call per folder (no per-file API calls)
tree = api.list_repo_tree(repo_id, path=date_folder, recursive=False)
files = sorted(
    f.rfilename
    for f in tree
    if f.rfilename.endswith((".jsonl", ".parquet", ".json"))
)

manifest = {"repo": repo_id, "date": date_folder, "files": files}
os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(files)} files to {out_path}")
PY