#!/usr/bin/env bash
# bin/snapshot.sh
# Pre-flight snapshot: list dataset files once → JSON for zero-API training
# Usage: HF_TOKEN=... ./bin/snapshot.sh [--date YYYY-MM-DD] [--out snapshot.json]
#   or:  ./bin/snapshot.sh 2026-05-02

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE=""
OUT=""

# Parse args: support both positional and flags
while [[ $# -gt 0 ]]; do
  case $1 in
    --date|-d) DATE="$2"; shift 2 ;;
    --out|-o)  OUT="$2";  shift 2 ;;
    *)         DATE="$1"; shift ;;
  esac
done

DATE="${DATE:-$(date +%Y-%m-%d)}"
OUT="${OUT:-snapshot-$(date +%Y%m%d).json}"

echo "📸 Snapshotting ${REPO} for ${DATE} → ${OUT}"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import os, json, sys
from datetime import datetime, timezone
from huggingface_hub import HfApi, hf_hub_url

repo = sys.argv[1]
date = sys.argv[2]
outfile = sys.argv[3]
token = os.environ.get("HF_TOKEN") or os.environ.get("HF_API_TOKEN") or None

api = HfApi(token=token)

def list_files(path):
    """List files at path (non-recursive) and return list of dicts."""
    items = api.list_repo_tree(repo=repo, path=path, recursive=False)
    files = []
    for item in items:
        if item.type == "file":
            full = f"{path}/{item.path}" if path != item.path else item.path
            cdn = hf_hub_url(repo_id=repo, filename=full, repo_type="dataset")
            direct = cdn.replace("/api/", "/resolve/")
            files.append({"path": full, "cdn_url": direct, "size": getattr(item, "size", None)})
        elif item.type == "folder":
            subpath = f"{path}/{item.path}" if path != item.path else item.path
            files.extend(list_files(subpath))
    return files

files = list_files(date)

result = {
    "repo": repo,
    "date": date,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "file_count": len(files),
    "files": files
}

with open(outfile, "w") as f:
    json.dump(result, f, indent=2)

print(f"✅ Snapshot written to {outfile} ({len(files)} files)")
PY