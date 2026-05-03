#!/usr/bin/env bash
# bin/snapshot.sh
# Usage: HF_TOKEN=... ./bin/snapshot.sh --repo axentx/surrogate-1-training-pairs --date 2026-05-02 --out snapshot.json
set -euo pipefail

REPO=""
DATE=""
OUT="snapshot.json"

while [[ $# -gt 0 ]]; do
  case $1 in
    --repo) REPO="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --out)  OUT="$2";  shift 2 ;;
    *) echo "Unknown option $1"; exit 1 ;;
  esac
done

if [[ -z "$REPO" || -z "$DATE" ]]; then
  echo "Usage: $0 --repo owner/repo --date YYYY-MM-DD [--out snapshot.json]"
  exit 1
fi

# Single API call: list top-level folder for the date (non-recursive)
# Avoids recursive list_repo_files which paginates 100x and hits rate limits.
echo "Listing ${REPO} for date ${DATE}..."
FILES=$(python3 - "$REPO" "$DATE" <<'PY'
import os, json, sys
from huggingface_hub import HfApi
api = HfApi(token=os.environ.get("HF_TOKEN"))
repo, date = sys.argv[1], sys.argv[2]
items = api.list_repo_tree(repo=repo, path=date, recursive=False)
# Expecting files directly under date folder: batches/mirror-merged/2026-05-02/*.parquet
result = []
for item in items:
    if item.type == "file" and item.path.endswith(".parquet"):
        result.append({
            "path": item.path,
            "size": item.size,
            "cdn_url": f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
        })
print(json.dumps(result, indent=2))
PY
)

echo "$FILES" > "$OUT"
echo "Snapshot written to $OUT ($(echo "$FILES" | jq length) files)"