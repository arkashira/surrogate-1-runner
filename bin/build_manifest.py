#!/usr/bin/env python3
"""
Generate manifest.json for a single date folder.
Run from Mac/CI (once per cron tick) to avoid HF API rate limits in workers.
"""
import json, os, sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

REPO = "datasets/axentx/surrogate-1-training-pairs"
DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
OUT = "manifest.json"

def main():
    api = HfApi()
    # Single API call: non-recursive, one folder
    entries = api.list_repo_tree(
        repo_id=REPO,
        path=f"batches/public-raw/{DATE}",
        repo_type="dataset",
        recursive=False,
    )
    files = [e.path for e in entries if e.path.endswith((".jsonl", ".parquet"))]
    manifest = {"date": DATE, "files": sorted(files)}
    with open(OUT, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {OUT} with {len(files)} files for {DATE}")

if __name__ == "__main__":
    main()