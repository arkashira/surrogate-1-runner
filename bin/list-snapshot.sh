#!/usr/bin/env bash
# Usage: list-snapshot.sh <date> [repo]
# Example: list-snapshot.sh 2026-05-02 axentx/surrogate-1-training-pairs
set -euo pipefail

DATE="${1:-}"
REPO="${2:-axentx/surrogate-1-training-pairs}"
OUTDIR="snapshot/${DATE}"
OUTFILE="${OUTDIR}/file-list.json"

if [[ -z "$DATE" ]]; then
  echo "Usage: $0 <date> [repo]" >&2
  exit 1
fi

mkdir -p "$OUTDIR"

# Single API call: list top-level folder for this date (non-recursive)
python3 - "$REPO" "$DATE" "$OUTFILE" <<'PY'
import json, os, sys
from huggingface_hub import HfApi

repo_id = sys.argv[1]
date = sys.argv[2]
outfile = sys.argv[3]

api = HfApi()
tree = api.list_repo_tree(repo_id=repo_id, path=date, recursive=False)
files = [{"path": t.path, "size": getattr(t, "size", None)} for t in tree if not t.path.endswith("/")]

with open(outfile, "w", encoding="utf-8") as f:
    json.dump({"date": date, "repo": repo_id, "files": files}, f, indent=2)

print(f"Wrote {len(files)} files to {outfile}")
PY

echo "Snapshot created: $OUTFILE"