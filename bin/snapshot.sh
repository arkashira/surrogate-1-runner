#!/usr/bin/env bash
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
OUT_DIR="snapshots"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%H%M%S)

mkdir -p "$OUT_DIR"

python3 - <<PY
import json, os, sys, time
from huggingface_hub import HfApi, RepositoryError

repo = os.environ["REPO"]
out_dir = os.environ["OUT_DIR"]
date = os.environ["DATE"]
timestamp = os.environ["TIMESTAMP"]

api = HfApi()
max_retries = 3
backoff = 360  # seconds

for attempt in range(max_retries):
    try:
        # Non-recursive to avoid pagination explosion
        date_tree = api.list_repo_tree(
            repo=repo, path=date, repo_type="dataset", recursive=False
        )
        break
    except RepositoryError as e:
        if attempt == max_retries - 1:
            print(f"Failed after {max_retries} attempts: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Rate limited (429), sleeping {backoff}s...", file=sys.stderr)
        time.sleep(backoff)

files = [item.rfilename for item in date_tree if not item.rfilename.endswith("/")]

snapshot = {
    "repo": repo,
    "date": date,
    "generated_at": f"{date}T{timestamp}",
    "files": sorted(files)
}

latest_path = os.path.join(out_dir, "snapshot-latest.json")
dated_path = os.path.join(out_dir, f"snapshot-{date}-{timestamp}.json")

os.makedirs(out_dir, exist_ok=True)
with open(latest_path, "w") as f:
    json.dump(snapshot, f, indent=2)
with open(dated_path, "w") as f:
    json.dump(snapshot, f, indent=2)

# Symlink latest for convenience
os.symlink(os.path.basename(dated_path), os.path.join(out_dir, "snapshot-latest.json"), 
           target_is_directory=False, dir_fd=None)

print(f"Snapshot written: {latest_path} ({len(files)} files)")
PY

echo "Snapshot complete."