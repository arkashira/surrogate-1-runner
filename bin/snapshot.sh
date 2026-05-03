#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
OUTDIR="${2:-snapshots}"
DATE_TAG=$(date +%Y%m%d)
OUTFILE="${OUTDIR}/snapshot-${DATE_TAG}.json"

mkdir -p "${OUTDIR}"

python3 - <<PY
import os, json, sys, datetime
from huggingface_hub import HfApi

repo = os.environ.get("REPO", "$REPO")
outfile = os.environ.get("OUTFILE", "$OUTFILE")
base_path = os.environ.get("BASE_PATH", "public-merged")

api = HfApi()
entries = []

try:
    # List top-level folders (date folders) then files within each
    tree = api.list_repo_tree(repo=repo, recursive=False, path=base_path)
    for item in tree:
        if item.type == "directory":
            subpath = item.path
            subfiles = api.list_repo_tree(repo=repo, recursive=False, path=subpath)
            for f in subfiles:
                if f.type == "file":
                    entries.append({
                        "repo": repo,
                        "path": f.path,
                        "size": f.size,
                        "sha": f.bin_sha if hasattr(f, "bin_sha") else None,
                        "cdn_url": f"https://huggingface.co/datasets/{repo}/resolve/main/{f.path}"
                    })
        elif item.type == "file":
            entries.append({
                "repo": repo,
                "path": item.path,
                "size": item.size,
                "sha": item.bin_sha if hasattr(item, "bin_sha") else None,
                "cdn_url": f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
            })
except Exception as e:
    print(f"Error listing repo: {e}", file=sys.stderr)
    sys.exit(1)

output = {
    "repo": repo,
    "date": datetime.date.today().isoformat(),
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    "files": entries
}

with open(outfile, "w") as f:
    json.dump(output, f, indent=2)
print(outfile)
PY