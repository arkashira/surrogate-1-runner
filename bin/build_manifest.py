#!/usr/bin/env python3
"""
Generate train_manifest.json for a given date folder.
Run from Mac (or any machine) after HF API rate-limit window clears.
"""
import json, os, sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

REPO = "datasets/axentx/surrogate-1-training-pairs"
DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime("%Y-%m-%d")
OUT = "train_manifest.json"

api = HfApi()
# Single API call: non-recursive listing for one date folder
tree = api.list_repo_tree(repo_id=REPO, path=DATE, recursive=False)
files = [f.rfilename for f in tree if f.rfilename.endswith((".parquet", ".jsonl", ".json"))]

manifest = {
    "date": DATE,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "files": sorted(files),
}

with open(OUT, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Wrote {OUT} with {len(files)} files for {DATE}")