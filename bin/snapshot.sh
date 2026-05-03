#!/usr/bin/env bash
# bin/snapshot.sh
# Generate a deterministic file manifest for a dataset repo + date folder.
#
# Usage:
#   REPO=axentx/surrogate-1-training-pairs DATE=2026-04-29 ./bin/snapshot.sh
#
# Outputs: snapshots/snapshot-<repo_slug>-<DATE>.json
# Requires: python3, huggingface_hub

set -euo pipefail

REPO="${REPO:-}"
DATE="${DATE:-}"
OUTDIR="${OUTDIR:-./snapshots}"

if [[ -z "$REPO" ]]; then
  echo "ERROR: REPO is required (e.g. axentx/surrogate-1-training-pairs)" >&2
  exit 1
fi

if [[ -z "$DATE" ]]; then
  DATE=$(date -u -d 'yesterday' '+%Y-%m-%d' 2>/dev/null || date -u -v-1d '+%Y-%m-%d')
  echo "INFO: DATE not provided, defaulting to $DATE" >&2
fi

REPO_SLUG=$(echo "$REPO" | tr '/-' '__')
mkdir -p "$OUTDIR"
OUTPUT="${OUTDIR}/snapshot-${REPO_SLUG}-${DATE}.json"

python3 - "$REPO" "$DATE" "$OUTPUT" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone

try:
    from huggingface_hub import HfApi
except ImportError:
    print("ERROR: huggingface_hub not installed. pip install huggingface_hub", file=sys.stderr)
    sys.exit(1)

repo = sys.argv[1]
date_folder = sys.argv[2].rstrip('/')
output_path = sys.argv[3]

api = HfApi()
path = date_folder  # top-level date folder inside dataset repo

try:
    entries = api.list_repo_tree(repo=repo, path=path, recursive=False)
except Exception as e:
    print(f"ERROR: failed to list repo tree for {repo}/{path}: {e}", file=sys.stderr)
    sys.exit(1)

files = sorted([e.path for e in entries if not e.path.endswith('/')])

manifest = {
    "repo": repo,
    "date": date_folder,
    "path_prefix": path,
    "files": files,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "note": "Use CDN URLs for training: https://huggingface.co/datasets/{repo}/resolve/main/{file}"
}

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
print(f"INFO: snapshot written to {output_path} ({len(files)} files)")
PY

echo "INFO: snapshot created at $OUTPUT"