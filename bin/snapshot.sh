#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE="${2:-$(date +%Y-%m-%d)}"
OUT="${3:-snapshot-${REPO//\//-}-${DATE}.json}"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json, sys, datetime
from huggingface_hub import HfApi

repo, date, out = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi()

try:
    files = api.list_repo_tree(repo=repo, path=date, recursive=False)
except Exception as e:
    print(f"ERROR: failed to list repo tree: {e}", file=sys.stderr)
    sys.exit(1)

manifest = {
    "repo": repo,
    "date": date,
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    "files": []
}

for f in files:
    if f.type != "file":
        continue
    path = f.rfilename
    manifest["files"].append({
        "path": path,
        "cdn_url": f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"
    })

if not manifest["files"]:
    print(f"ERROR: no files found in {repo} at {date}", file=sys.stderr)
    sys.exit(1)

with open(out, "w") as fh:
    json.dump(manifest, fh, indent=2)
print(out)
PY