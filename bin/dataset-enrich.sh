# Accept MANIFEST_JSON env or arg.
# Downloads via CDN (no auth/API) and projects to {prompt,response}.

set -euo pipefail

MANIFEST="${MANIFEST_JSON:-}"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
OUT_DIR="output"
mkdir -p "$OUT_DIR"

if [ -z "$MANIFEST" ] || [ ! -f "$MANIFEST" ]; then
  echo "MANIFEST_JSON must point to a valid manifest file"
  exit 1
fi

# Deterministic shard assignment by file path hash
python3 - "$MANIFEST" "$SHARD_ID" "$TOTAL_SHARDS" "$OUT_DIR" <<'PY'
import json, hashlib, os, sys, subprocess, tempfile, itertools, pyarrow.parquet as pq

manifest_path, shard_id, total_shards, out_dir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
shard_id = int(shard_id)

with open(manifest_path) as f:
    manifest = json.load(f)

files = manifest["files"]
os.makedirs(out_dir, exist_ok=True)

def assign_shard(path: str) -> int:
    h = int(hashlib.md5(path.encode()).hexdigest(), 16)
    return h % total_shards

selected = [f for f in files if assign_shard(f["path"]) == shard_id]
print(f"Shard {shard_id}/{total_shards}: processing {len(selected)} files")

def normalize_to_pairs(file_info):
    url = file_info["cdn_url"]
    path = file_info["path"]
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(path)[1], delete=False) as tmp:
        # CDN download (no auth)
        subprocess.run(["curl", "-fsSL", "-o", tmp.name, url], check=True)
        tmp_path = tmp.name
    try:
        # Project to prompt/response only; ignore extra columns
        if path.endswith(".parquet"):
            table = pq.read_table(tmp_path, columns=["prompt", "response"])
            df = table.to_pandas()
        elif path.endswith(".jsonl"):
            import pandas as pd
            df = pd.read_json(tmp_path, lines=True)
            if "prompt" not in df.columns or "response" not in df.columns:
                # Best-effort column selection
                df = df.rename(columns={c: c.lower() for c in df.columns})
                if "prompt" not in df.columns or "response" not in df.columns:
                    return []
        else:
            # CSV fallback
            import pandas as pd
            df = pd.read_csv(tmp_path)
            df.columns = [c.lower() for c in df.columns]

        pairs = []
        for _, row in df.iterrows():
            prompt = str(row.get("prompt", ""))
            response = str(row.get("response", ""))
            if prompt.strip() and response.strip():
                pairs.append({"prompt": prompt, "response": response})
        return pairs
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

all_pairs = []
for f in selected:
    try:
        pairs = normalize_to_pairs(f)
        all_pairs.extend(pairs)
    except Exception as exc:
        print(f"Failed {f['path']}: {exc}")

ts = manifest["created_at"].replace(":", "").split("T")[0]
out_file = os.path.join(out_dir, f"shard{shard_id}-{ts}.jsonl")
with open(out_file, "w", encoding="utf-8") as f:
    for p in all_pairs:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")

print(f"Shard {shard_id} wrote {len(all_pairs)} pairs to {out_file}")
PY