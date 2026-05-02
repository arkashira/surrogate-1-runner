#!/usr/bin/env bash
# Mac-side orchestrator: run after HF API rate-limit window clears.
# Produces file-list-{date}.json and optional workflow_dispatch payload.
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
OUT_DIR="file-lists"
mkdir -p "$OUT_DIR"

# Requires: pip install huggingface_hub
python3 - "$REPO" "$OUT_DIR" <<'PY'
import json, os, sys
from datetime import datetime, timedelta
from huggingface_hub import HfApi

repo = sys.argv[1]
out_dir = sys.argv[2]
api = HfApi()

def date_folders():
    today = datetime.utcnow().date()
    for i in range(2):
        d = today - timedelta(days=i)
        yield d.strftime("%Y-%m-%d")

for folder in date_folders():
    try:
        # non-recursive to avoid pagination explosion
        nodes = api.list_repo_tree(repo=repo, path=folder, recursive=False)
        files = [n.rfilename for n in nodes if not n.rfilename.endswith("/")]
    except Exception as e:
        print(f"Skipping {folder}: {e}", file=sys.stderr)
        continue
    out_path = os.path.join(out_dir, f"file-list-{folder}.json")
    with open(out_path, "w") as f:
        json.dump({"date": folder, "files": files}, f)
    print(f"Wrote {len(files)} files -> {out_path}")
PY

# Optional: create workflow_dispatch matrix payload
cat > payload.json <<EOF
{
  "ref": "main",
  "inputs": {
    "file_list_artifact": "$(ls -1 "$OUT_DIR"/file-list-*.json | head -1)"
  }
}
EOF
echo "To trigger: gh workflow run ingest.yml --json '$(<payload.json)'"