#!/usr/bin/env bash
set -euo pipefail

REPO="datasets/axentx/surrogate-1-training-pairs"
OUTDIR="${1:-.}"
DATE="${2:-$(date +%Y-%m-%d)}"
OUTFILE="${OUTDIR}/snapshot-${DATE}.json"

python3 - "$REPO" "$DATE" "$OUTFILE" <<'PY'
import json, sys
from huggingface_hub import HfApi

repo_id, date = sys.argv[1], sys.argv[2]
outfile = sys.argv[3]
api = HfApi()

# Non-recursive list to avoid pagination explosion
items = api.list_repo_tree(repo_id, path=f"public-merged/{date}", recursive=False)
files = []
for item in items:
    if item.type == "file":
        files.append({
            "path": item.path,
            "size": item.size,
            "sha256": getattr(item, "sha256", None)
        })

snapshot = {
    "repo": repo_id,
    "date": date,
    "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "files": files
}

with open(outfile, "w") as f:
    json.dump(snapshot, f, indent=2)
print(f"Wrote {len(files)} files to {outfile}")
PY

echo "Snapshot saved: $OUTFILE"