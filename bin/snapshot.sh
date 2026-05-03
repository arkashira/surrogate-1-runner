#!/usr/bin/env bash
# bin/snapshot.sh
#
# Generate a deterministic file manifest for a date folder in
# axentx/surrogate-1-training-pairs so training can use HF CDN only.
#
# Usage:
#   HF_TOKEN=hf_xxx ./bin/snapshot.sh 2026-05-03
#
# Outputs:
#   snapshots/2026-05-03-manifest.json
#   snapshots/2026-05-03-manifest.json.sha256
#   snapshots/2026-05-03-manifest.files.txt

set -euo pipefail

REPO="datasets/axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTDIR="snapshots"
MANIFEST="${OUTDIR}/${DATE}-manifest.json"

mkdir -p "${OUTDIR}"

echo "== Generating snapshot for ${DATE} =="

python3 - <<PY
import os, json, sys
from huggingface_hub import HfApi

api = HfApi(token=os.environ.get("HF_TOKEN"))
repo = "datasets/axentx/surrogate-1-training-pairs"
date = sys.argv[1]

# Non-recursive list to avoid pagination/429 on large repos
entries = api.list_repo_tree(repo=repo, path=date, recursive=False)

files = []
for e in entries:
    if e.type == "file":
        files.append({
            "path": f"{date}/{e.path.split('/')[-1]}",
            "size": getattr(e, "size", None),
            "lfs": getattr(e, "lfs", None) is not None,
        })

# Deterministic ordering
files.sort(key=lambda x: x["path"])

manifest = {
    "date": date,
    "repo": repo,
    "generated_at_utc": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "files": files,
    "cdn_base": f"https://huggingface.co/datasets/{repo}/resolve/main",
}

out_path = sys.argv[2]
with open(out_path, "w") as f:
    json.dump(manifest, f, indent=2, sort_keys=True)

# Compact line-delimited variant for shell loops
lines_path = out_path.replace(".json", ".files.txt")
with open(lines_path, "w") as f:
    for item in files:
        f.write(f"{item['path']}\n")

print(f"Wrote {len(files)} files -> {out_path}")
PY "${DATE}" "${MANIFEST}"

# Create checksum
sha256sum "${MANIFEST}" > "${MANIFEST}.sha256"
echo "== Snapshot complete: ${MANIFEST} (+ .sha256 + .files.txt) =="