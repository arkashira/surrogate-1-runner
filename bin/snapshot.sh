#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-axentx/surrogate-1-training-pairs}"
HF_TOKEN="${HF_TOKEN:?ERROR: HF_TOKEN required}"
DATE=""
SHARD=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date) DATE="$2"; shift 2 ;;
    --repo) REPO="$2"; shift 2 ;;
    --shard) SHARD="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

[[ -z "$DATE" ]] && { echo "ERROR: --date required" >&2; exit 1; }

BASE_PATH="batches/public-merged/${DATE}"
TMP=$(mktemp)

python3 - "$REPO" "$BASE_PATH" "$HF_TOKEN" "$TMP" <<'PY'
import json, sys, hashlib, datetime
from huggingface_hub import HfApi

repo_id, path, token, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
api = HfApi(token=token)
tree = api.list_repo_tree(repo_id=repo_id, path=path, recursive=False)

files = []
shards = {str(i): [] for i in range(16)}

for item in tree:
    if getattr(item, "type", None) != "file":
        continue
    p = item.path
    if not (p.endswith(".jsonl") or p.endswith(".parquet")):
        continue
    cdn = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{p}"
    entry = {
        "path": p,
        "cdn_url": cdn,
        "size": getattr(item, "size", None),
        "md5": getattr(item, "lfs", {}).get("oid", None) if hasattr(item, "lfs") else None,
        "etag": getattr(item, "etag", None)
    }
    files.append(entry)

    slug = p.split("/")[-1].rsplit(".", 1)[0]
    shard_id = str(abs(hash(slug)) % 16)
    if shard_id in shards:
        shards[shard_id].append(p)

files.sort(key=lambda x: x["path"])
for k in shards:
    shards[k].sort()

result = {
    "date": path.split("/")[-1],
    "repo": repo_id,
    "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    "cdn_base": f"https://huggingface.co/datasets/{repo_id}/resolve/main",
    "base_path": path,
    "files": files,
    "shards": shards
}

# canonical sha256
canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
result["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()

with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, sort_keys=False)
PY

# Optional shard filter (post-process)
if [[ -n "$SHARD" ]]; then
  python3 - "$TMP" "$SHARD" <<'PY'
import json, sys
with open(sys.argv[1]) as f:
    d = json.load(f)
sid = sys.argv[2]
d["files"] = [f for f in d["files"] if f"shard{sid}-" in f["path"]]
with open(sys.argv[1], "w") as f:
    json.dump(d, f, indent=2)
PY
fi

if [[ -n "$OUTPUT" ]]; then
  mv "$TMP" "$OUTPUT"
  echo "Snapshot: $OUTPUT" >&2
else
  cat "$TMP"
  rm -f "$TMP"
fi