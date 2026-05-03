#!/usr/bin/env bash
set -euo pipefail
# snapshot.sh — list dataset files once for CDN-only training
# Usage: ./bin/snapshot.sh --repo <owner>/<dataset> --date YYYY-MM-DD [--out <path>] [--dry-run]

REPO=""
DATE=""
OUT=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)  REPO="$2"; shift 2 ;;
    --date)  DATE="$2"; shift 2 ;;
    --out)   OUT="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    *) echo "Unknown option $1"; exit 1 ;;
  esac
done

: "${REPO:?required}"
: "${DATE:?required}"
OUT="${OUT:-snapshot-${DATE}.json}"

python3 - <<PY
import os, json, sys, time
from huggingface_hub import HfApi
from datetime import datetime

repo = "${REPO}"
date = "${DATE}"
out = "${OUT}"
dry_run = ${DRY_RUN}
api = HfApi()

try:
    tree = api.list_repo_tree(repo=repo, path=date, repo_type="dataset", recursive=False)
except Exception as e:
    if "429" in str(e):
        print("Rate limited (429). Wait 360s before retry.", file=sys.stderr)
    sys.exit(1)

files = [{"path": f.rfilename, "size": getattr(f, "size", None)} for f in tree if f.rfilename]
snapshot = {
    "repo": repo,
    "date": date,
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "files": files
}

if dry_run:
    print(f"[dry-run] Would write {len(files)} files to {out}")
    sys.exit(0)

os.makedirs(os.path.dirname(out) if os.path.dirname(out) else ".", exist_ok=True)
with open(out, "w") as fp:
    json.dump(snapshot, fp, indent=2)

print(f"Snapshot written to {out} ({len(files)} files)")
PY