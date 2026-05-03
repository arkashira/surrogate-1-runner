#!/usr/bin/env bash
set -euo pipefail

REPO="${HF_REPO:-axentx/surrogate-1-training-pairs}"
DATE="${1:-$(date +%Y-%m-%d)}"
OUTDIR="${2:-snapshots}"
OUT="${OUTDIR}/snapshot-${DATE}.json"

mkdir -p "${OUTDIR}"

python3 - <<PY
import os, json, datetime, sys
from huggingface_hub import HfApi

repo = os.getenv("HF_REPO", "axentx/surrogate-1-training-pairs")
date = os.getenv("SNAPSHOT_DATE", datetime.date.today().isoformat())
out = os.getenv("SNAPSHOT_OUT", "snapshots/snapshot-{}.json".format(date))

api = HfApi(token=os.getenv("HF_TOKEN"))
try:
    tree = api.list_repo_tree(repo=repo, path=date, recursive=False)
except Exception as e:
    # If folder missing, produce empty snapshot so runners skip cleanly
    files = []
else:
    files = [{"path": f.rfilename, "size": getattr(f, "size", None)} for f in tree]

os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as fh:
    json.dump({"date": date, "ts": datetime.datetime.utcnow().isoformat() + "Z", "files": files}, fh)
print(f"Wrote {len(files)} entries to {out}")
PY

echo "Snapshot created: ${OUT}"