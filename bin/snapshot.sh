#!/usr/bin/env bash
# bin/snapshot.sh
# Generate CDN snapshot for surrogate-1 dataset ingestion.
# Usage: HF_TOKEN=... ./bin/snapshot.sh <date> [output.json]

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="${2:-snapshot-${DATE}.json}"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json, os, sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

repo, date, out = sys.argv[1], sys.argv[2], sys.argv[3]
api = HfApi(token=os.getenv("HF_TOKEN"))

# List top-level date folders (non-recursive)
tree = api.list_repo_tree(repo, path="", recursive=False)
folders = [t for t in tree if t.type == "directory" and t.path.startswith(date)]

if not folders:
    print(f"No folders found for date {date}", file=sys.stderr)
    sys.exit(1)

entries = []
for f in folders:
    files = api.list_repo_tree(repo, path=f.path, recursive=False)
    for file in files:
        if file.type == "file" and file.path.endswith((".parquet", ".jsonl")):
            cdn_url = f"https://huggingface.co/datasets/{repo}/resolve/main/{file.path}"
            entries.append({
                "path": file.path,
                "cdn_url": cdn_url,
                "size": getattr(file, "size", None)
            })

# Deterministic ordering
entries.sort(key=lambda x: x["path"])

snapshot = {
    "repo": repo,
    "date": date,
    "ts": datetime.now(timezone.utc).isoformat(),
    "files": entries
}

with open(out, "w") as fp:
    json.dump(snapshot, fp, indent=2)

print(f"Snapshot written to {out} ({len(entries)} files)")
PY