#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... ./bin/snapshot.sh <date> [out.json]
# Example: ./bin/snapshot.sh 2026-05-03 snapshots/public-merged/2026-05-03/manifest.json

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="${2:-snapshots/public-merged/${DATE}/manifest.json}"
HF_TOKEN="${HF_TOKEN:-}"

if [ -z "$HF_TOKEN" ]; then
  echo "ERROR: HF_TOKEN is required" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import os, json, sys
from huggingface_hub import HfApi

repo = sys.argv[1]
date = sys.argv[2]
out_path = sys.argv[3]
token = os.environ["HF_TOKEN"]

api = HfApi(token=token)

# Single non-recursive call
tree = api.list_repo_tree(
    repo_id=repo,
    path=f"batches/public-merged/{date}",
    repo_type="dataset",
    recursive=False
)

manifest = []
for item in tree:
    if item.path.rstrip("/").endswith("/"):
        continue  # skip directory entries
    manifest.append({
        "path": item.path,
        "size": getattr(item, "size", None),
        "lfs": getattr(item, "lfs", None),
    })

# Deterministic ordering
manifest.sort(key=lambda x: x["path"])

with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"repo": repo, "date": date, "files": manifest}, f, indent=2, sort_keys=True)

print(f"Wrote {len(manifest)} entries to {out_path}")
PY