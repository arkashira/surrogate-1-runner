#!/usr/bin/env bash
set -euo pipefail

: "${SHARD_ID:?}"
: "${DATE_PART:?}"
: "${TIME_PART:?}"
: "${REPO:?}"
: "${HF_TOKEN:?}"

BASE_OUT="batches/public-merged/${DATE_PART}"
OUT_FILE="${BASE_OUT}/shard${SHARD_ID}-${TIME_PART}.jsonl"
SUCCESS_MARKER="${BASE_OUT}/shard${SHARD_ID}-${TIME_PART}.success"

mkdir -p "$(dirname "$OUT_FILE")"

# Skip if this exact shard/time already completed (avoid races/repeats)
if [[ -f "$SUCCESS_MARKER" ]]; then
  echo "Shard ${SHARD_ID} for ${DATE_PART} ${TIME_PART} already done (success marker present). Skipping."
  exit 0
fi

# Deterministic shard assignment by slug
shard_for() {
  local slug=$1
  python -c "import hashlib; print(abs(int(hashlib.sha256('$slug'.encode()).hexdigest(), 16)) % 16)"
}

python - <<PY
import json, os, hashlib, sys, requests, tqdm

SHARD_ID = int(os.getenv("SHARD_ID"))
REPO = os.getenv("REPO")
OUT_FILE = os.getenv("OUT_FILE")
FILE_LIST = "file-list.json"

with open(FILE_LIST) as f:
    manifest = json.load(f)

files = manifest["files"]

def shard_for(slug: str) -> int:
    return abs(int(hashlib.sha256(slug.encode()).hexdigest(), 16)) % 16

def download_cdn(path: str) -> bytes:
    url = f"https://huggingface.co/datasets/{REPO}/resolve/main/{path}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.content

def parse_to_pair(raw: bytes, filename: str):
    # Adapt to your schema. Must return dict with at least {prompt,response}.
    text = raw.decode("utf-8", errors="replace")
    return {"prompt": f"from {filename}", "response": text[:2000]}

written = 0
with open(OUT_FILE, "w", encoding="utf-8") as out:
    for fpath in tqdm.tqdm(files, desc="Processing"):
        slug = os.path.splitext(os.path.basename(fpath))[0]
        if shard_for(slug) != SHARD_ID:
            continue
        try:
            raw = download_cdn(fpath)
            pair = parse_to_pair(raw, fpath)
            if pair is None:
                continue
            pair["_md5"] = hashlib.md5(raw).hexdigest()
            pair["_source_file"] = fpath
            out.write(json.dumps(pair, ensure_ascii=False) + "\n")
            written += 1
        except Exception as e:
            print(f"WARN: failed {fpath}: {e}", file=sys.stderr)

print(f"Wrote {written} pairs to {OUT_FILE}")
PY

# Create success marker to prevent re-runs/races for this exact shard/time
touch "$SUCCESS_MARKER"

# Push only this shard's file + marker
git config user.name "github-actions"
git config user.email "github-actions@github.com"
git add "$OUT_FILE" "$SUCCESS_MARKER"
git commit -m "shard${SHARD_ID} ${DATE_PART} ${TIME_PART}" || true
git push "https://${HF_TOKEN}@huggingface.co/datasets/${REPO}.git" HEAD:main