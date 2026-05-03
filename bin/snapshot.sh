#!/usr/bin/env bash
# bin/snapshot.sh
# Generate deterministic file-list snapshot for CDN-only ingestion.
# Usage: HF_TOKEN=<token> bin/snapshot.sh <owner>/<dataset> <date-folder>

set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
DATE="${2:-$(date +%Y-%m-%d)}"
OUTDIR="snapshot/${DATE}"
OUTFILE="${OUTDIR}/file-list.json"

mkdir -p "${OUTDIR}"

echo "Listing ${REPO} (non-recursive) for date folder: ${DATE}..."

# Use huggingface_hub Python to list top-level folder (avoids recursive pagination)
python3 - <<PY > "${OUTFILE}.tmp"
import os, json
from huggingface_hub import HfApi

api = HfApi(token=os.environ.get("HF_TOKEN"))
repo = "${REPO}"
date_folder = "${DATE}"

# List only the date folder (non-recursive)
tree = api.list_repo_tree(repo=repo, path=date_folder, recursive=False)

files = []
for item in tree:
    if item.type == "file":
        # CDN URL (no auth required)
        cdn_url = f"https://huggingface.co/datasets/{repo}/resolve/main/{date_folder}/{item.path}"
        files.append({
            "path": item.path,
            "cdn_url": cdn_url,
            "size": getattr(item, "size", None)
        })

# Deterministic ordering
files.sort(key=lambda x: x["path"])

output = {
    "repo": repo,
    "date": date_folder,
    "generated_at": os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip(),
    "files": files
}

print(json.dumps(output, indent=2))
PY

mv "${OUTFILE}.tmp" "${OUTFILE}"
echo "Snapshot written to ${OUTFILE}"
echo "Total files: $(jq '.files | length' "${OUTFILE}")"