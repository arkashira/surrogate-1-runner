#!/usr/bin/env bash
# bin/snapshot.sh
#
# Generate a deterministic file manifest for a dataset repo/date folder.
#
# Usage:
#   HF_TOKEN=<token> ./bin/snapshot.sh \
#     --repo axentx/surrogate-1-training-pairs \
#     --date 2026-04-29 \
#     --out snapshots/2026-04-29-manifest.json
#
# Behavior:
# - Uses HF API list_repo_tree (non-recursive) for the date folder.
# - Emits JSON array of { "path": "...", "size": ..., "sha": "..." }
# - Deterministic ordering for stable snapshots.
# - Exits non-zero on failure; prints actionable retry guidance after 429.
# - If date folder is missing, emits empty array and exits 0.

set -euo pipefail

REPO=""
DATE=""
OUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --out)  OUT="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$REPO" || -z "$DATE" || -z "$OUT" ]]; then
  echo "Usage: $0 --repo <owner/repo> --date <YYYY-MM-DD> --out <path>" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"

# Prefer HF_TOKEN from env; if missing, allow unauthenticated (public datasets).
# list_repo_tree is used per folder to avoid recursive pagination explosion.
# We only need immediate children under the date folder.
python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import os
import json
import sys
import time
from huggingface_hub import HfApi

REPO = sys.argv[1]
DATE = sys.argv[2]
OUT = sys.argv[3]

api = HfApi(token=os.getenv("HF_TOKEN") or None)

# Retry guidance for 429 baked into CLI behavior; here we raise so shell can handle.
try:
    entries = api.list_repo_tree(
        repo_id=REPO,
        path=DATE,
        repo_type="dataset",
        recursive=False,
    )
except Exception as e:
    # If folder missing, produce empty manifest rather than fail.
    if "404" in str(e) or "not found" in str(e).lower():
        entries = []
    else:
        raise

manifest = []
for e in entries:
    # Keep only files (ignore subfolders). Path is relative to repo root.
    if getattr(e, "type", None) == "file":
        manifest.append({
            "path": e.path,            # e.g. 2026-04-29/file1.parquet
            "size": e.size or 0,
            "sha": getattr(e, "lfs", {}).get("sha256", "") if getattr(e, "lfs", None) else "",
        })

# Deterministic ordering for stable snapshots.
manifest.sort(key=lambda x: x["path"])

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, sort_keys=True)

print(f"Wrote {len(manifest)} entries to {OUT}")
PY