#!/usr/bin/env python3
"""
Fetch a flat file list for a single date folder from the HF dataset repo.
Usage:
  python bin/fetch-manifest.py 2026-05-03
"""
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

REPO_ID = "datasets/axentx/surrogate-1-training-pairs"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "manifests")

def main():
    date_folder = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    api = HfApi()
    # Non-recursive: one API call, paginated safely (100/page)
    files = api.list_repo_tree(repo_id=REPO_ID, path=date_folder, recursive=False)
    entries = []
    for f in files:
        if f.rfilename.endswith((".parquet", ".jsonl", ".json")):
            entries.append({
                "path": f.rfilename,
                "size": getattr(f, "size", None)
            })
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"manifest-{date_folder}.json")
    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump({"date_folder": date_folder, "files": entries}, fp, indent=2)
    print(f"Wrote {len(entries)} entries to {out_path}")

if __name__ == "__main__":
    main()