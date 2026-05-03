#!/usr/bin/env python3
"""
Generate train_manifest.json for a given date folder.
Run once per day (or per cron) on a Mac/CI with HF_TOKEN.
"""
import os, json, datetime
from huggingface_hub import HfApi

API = HfApi()
REPO = "axentx/surrogate-1-training-pairs"
DATE = datetime.date.today().isoformat()  # e.g. 2026-05-03
MANIFEST = "train_manifest.json"

def main() -> None:
    entries = API.list_repo_tree(
        repo_id=REPO,
        path=f"batches/public-merged/{DATE}",
        recursive=False,
    )
    files = [e.path for e in entries if e.path.endswith(".parquet")]
    manifest = {"date": DATE, "files": sorted(files)}
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {MANIFEST} with {len(files)} files for {DATE}")

if __name__ == "__main__":
    main()