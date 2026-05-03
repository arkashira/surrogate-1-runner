#!/usr/bin/env bash
# bin/snapshot.sh
#
# Pre-flight snapshot for surrogate-1 dataset ingestion.
#
# Usage:
#   HF_TOKEN=<token> ./bin/snapshot.sh \
#     --repo axentx/surrogate-1-training-pairs \
#     --date 2026-04-29 \
#     --out snapshots/2026-04-29-manifest.json
#
# Environment overrides:
#   REPO, DATE (YYYY-MM-DD), OUT, HF_TOKEN
#
# Behavior:
# - Lists files under {date}/ (non-recursive) via huggingface_hub.
# - Emits a deterministic JSON manifest with CDN URLs.
# - Manifest can be committed or embedded into training scripts.
# - CDN downloads bypass /api/ auth rate limits.

set -euo pipefail

REPO="${REPO:-}"
DATE="${DATE:-$(date +%Y-%m-%d)}"
OUT="${OUT:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --out)  OUT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$REPO" || -z "$OUT" ]]; then
  echo "Usage: $0 --repo <repo> --date <YYYY-MM-DD> --out <path>"
  echo "  Or set env: REPO=<repo> DATE=<YYYY-MM-DD> OUT=<path>"
  exit 1
fi

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "ERROR: HF_TOKEN is required to list repo tree." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone
from huggingface_hub import HfApi, hf_hub_url

def main(repo: str, date: str, out: str) -> None:
    api = HfApi(token=os.environ["HF_TOKEN"])
    # List only top-level entries for the date folder (non-recursive).
    entries = api.list_repo_tree(
        repo=repo,
        path=date,
        recursive=False,
        repo_type="dataset",
    )

    files = []
    for e in sorted(entries, key=lambda x: x.path):
        if e.type != "file":
            continue
        # CDN URL that bypasses /api/ auth checks.
        cdn_url = hf_hub_url(
            repo_id=repo,
            filename=e.path,
            repo_type="dataset",
        )
        # Convert to raw resolve URL (CDN).
        cdn_url = cdn_url.replace("/api/", "/resolve/")
        files.append({
            "path": e.path,
            "size": getattr(e, "size", None),
            "cdn_url": cdn_url,
        })

    manifest = {
        "repo": repo,
        "date": date,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "note": "CDN URLs bypass HF API auth rate limits during training data loading.",
    }

    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print(f"Wrote {len(files)} files to {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
PY