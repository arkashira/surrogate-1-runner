#!/usr/bin/env bash
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="snapshot-${DATE}.json"

echo "Listing dataset tree for public-merged/${DATE}/ ..."
python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json, sys
from huggingface_hub import HfApi

repo, date, out = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi()
path = f"public-merged/{date}"
try:
    tree = api.list_repo_tree(repo=repo, path=path, recursive=False)
except Exception as e:
    print(f"Error listing repo tree: {e}", file=sys.stderr)
    sys.exit(1)

files = [
    {
        "path": f.path,
        "cdn_url": f"https://huggingface.co/datasets/{repo}/resolve/main/{f.path}"
    }
    for f in tree if f.type == "file"
]

with open(out, "w") as f:
    json.dump({"date": date, "files": files}, f, indent=2)
print(f"Wrote {len(files)} files to {out}")
PY

echo "Snapshot saved to $OUT"