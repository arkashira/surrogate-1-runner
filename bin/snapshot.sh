#!/usr/bin/env bash
set -euo pipefail

# Usage: bin/snapshot.sh [YYYY-MM-DD]
# Generates snapshot-YYYY-MM-DD.json listing files under public-merged/<date>/

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="snapshot-${DATE}.json"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json
import sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

repo_id = sys.argv[1]
date_folder = sys.argv[2]
out_path = sys.argv[3]

api = HfApi()
path_prefix = f"public-merged/{date_folder}"
try:
    tree = api.list_repo_tree(repo_id=repo_id, path=path_prefix, recursive=False)
    files = [item.path for item in tree if item.type == "file"]
except Exception as e:
    # Fallback: try recursive=False per folder if path_prefix not found
    # If still fails, produce empty list so caller can fallback
    files = []

snapshot = {
    "date": date_folder,
    "repo": repo_id,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "files": sorted(files)
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(snapshot, f, indent=2)
print(f"Wrote {len(files)} files to {out_path}")
PY

echo "Snapshot written to $OUT"