#!/usr/bin/env bash
# bin/list-shards.sh
# Usage: HF_TOKEN=... ./bin/list-shards.sh [date] [--out FILE]
# Produces: shard-manifest.json
set -euo pipefail

REPO="datasets/axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="${2:-shard-manifest.json}"
SHARD_TOTAL="${SHARD_TOTAL:-16}"

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "ERROR: HF_TOKEN is required" >&2
  exit 1
fi

# Use Python for reliable JSON + HF API
python3 - "$DATE" "$OUT" "$SHARD_TOTAL" <<'PYEOF'
import json, os, sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

date_folder, out_path, shard_total = sys.argv[1], sys.argv[2], int(sys.argv[3])
api = HfApi()
repo = "datasets/axentx/surrogate-1-training-pairs"
prefix = f"{date_folder}/"

try:
    tree = api.list_repo_tree(
        repo_id=repo,
        path=prefix,
        recursive=False,
        repo_type="dataset",
    )
except Exception as e:
    print(f"ERROR listing repo tree: {e}", file=sys.stderr)
    sys.exit(1)

files = sorted(
    node.path
    for node in tree
    if node.type == "file" and node.path.lower().endswith((".jsonl", ".parquet"))
)

# Deterministic shard assignment by filename slug
def shard_for(path: str) -> int:
    slug = os.path.splitext(os.path.basename(path))[0]
    return hash(slug) % shard_total

shard_map = {}
for f in files:
    s = shard_for(f)
    shard_map.setdefault(str(s), []).append(f)

manifest = {
    "repo": repo,
    "date": date_folder,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "shard_total": shard_total,
    "shards": shard_map,
    "all_files": files,
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")

print(f"Wrote manifest for {len(files)} files across {len(shard_map)} shards to {out_path}")
PYEOF