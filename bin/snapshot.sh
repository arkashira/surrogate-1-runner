#!/usr/bin/env bash
# bin/snapshot.sh
# Generate deterministic file manifest for a dataset repo/date folder.
# Usage:
#   HF_TOKEN=<token> ./bin/snapshot.sh <repo_id> <date_path> [output.json]
# Example:
#   HF_TOKEN=$HF_TOKEN ./bin/snapshot.sh datasets/axentx/surrogate-1-training-pairs 2026-04-29 snapshot-2026-04-29.json

set -euo pipefail

REPO_ID="${1:-datasets/axentx/surrogate-1-training-pairs}"
DATE_PATH="${2:-$(date +%Y-%m-%d)}"
OUTPUT="${3:-}"

exec_python() {
  python3 - "$REPO_ID" "$DATE_PATH" "$OUTPUT" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

def main():
    if len(sys.argv) != 4:
        print("Usage: snapshot.py <repo_id> <date_path> <output|->", file=sys.stderr)
        sys.exit(1)
    repo_id = sys.argv[1]
    date_path = sys.argv[2].lstrip("/")
    output = sys.argv[3]

    api = HfApi(token=os.environ.get("HF_TOKEN"))
    entries = api.list_repo_tree(repo_id=repo_id, path=date_path, repo_type="dataset", recursive=False)

    files = []
    for e in sorted(entries, key=lambda x: x.path):
        if e.path.endswith("/"):
            continue
        files.append({
            "path": e.path,
            "size": getattr(e, "size", None),
            "lfs": getattr(e, "lfs", None),
            "sha": getattr(e, "sha", None),
        })

    manifest = {
        "repo_id": repo_id,
        "date_path": date_path,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(files),
        "files": files,
    }

    out = json.dumps(manifest, indent=2, sort_keys=True)
    if output == "-" or not output:
        print(out)
    else:
        os.makedirs(os.path.dirname(os.path.abspath(output)) if os.path.dirname(output) else ".", exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Wrote {len(files)} files to {output}", file=sys.stderr)

if __name__ == "__main__":
    main()
PY
}

exec_python