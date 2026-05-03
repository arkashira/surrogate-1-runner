#!/usr/bin/env bash
set -euo pipefail

REPO="${HF_DATASET_REPO:-axentx/surrogate-1-training-pairs}"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTFILE="${2:-file-list.json}"

# Requires huggingface_hub; install via pip if missing
python3 - "$REPO" "$DATE" "$OUTFILE" <<'PY'
import json, os, sys
from huggingface_hub import HfApi

repo, date, outfile = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi()
# Single non-recursive call per date folder
tree = api.list_repo_tree(repo=repo, path=date, recursive=False)
files = [f.rfilename for f in tree if f.rfilename.endswith(('.jsonl', '.parquet', '.csv'))]
with open(outfile, "w") as f:
    json.dump({"date": date, "files": files, "snapshot_ts": time.time()}, f, indent=2)
print(f"Snapshot written: {len(files)} files -> {outfile}")
PY