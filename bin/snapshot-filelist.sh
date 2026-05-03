#!/usr/bin/env bash
# bin/snapshot-filelist.sh
# Usage: HF_TOKEN=... ./bin/snapshot-filelist.sh [YYYY-MM-DD]
# Emits snapshots/filelist-YYYY-MM-DD.json with CDN-ready file paths.
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date -u +%Y-%m-%d)}"
OUT_DIR="$(cd "$(dirname "$0")/../snapshots" && pwd)"
OUT_FILE="${OUT_DIR}/filelist-${DATE}.json"

mkdir -p "$OUT_DIR"

python3 - "$REPO" "$DATE" "$OUT_FILE" <<'PY'
import os, json, sys
from huggingface_hub import HfApi

repo, date, out = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi(token=os.environ.get("HF_TOKEN"))

# Single non-recursive call per date folder
tree = api.list_repo_tree(repo, path=f"public-merged/{date}", recursive=False)
files = [item.rfilename for item in tree if item.type == "file"]
payload = {
    "date": date,
    "repo": repo,
    "snapshot_ts": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
    "files": sorted(files),
    "cdn_base": f"https://huggingface.co/datasets/{repo}/resolve/main"
}
with open(out, "w") as f:
    json.dump(payload, f, indent=2)
print(f"Snapshot saved: {out} ({len(files)} files)")
PY