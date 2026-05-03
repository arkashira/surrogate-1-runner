#!/usr/bin/env python3
"""
Generate a deterministic file manifest for a date folder in
axentx/surrogate-1-training-pairs.

Usage:
  python list_manifest.py --date 2026-05-01 > manifest-2026-05-01.json
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi

HF_REPO = "datasets/axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser(description="List files for a date folder.")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-01")
    parser.add_argument("--batches-dir", default="batches/public-merged", help="Subfolder prefix")
    args = parser.parse_args()

    api = HfApi()
    folder = f"{args.batches_dir}/{args.date}"
    try:
        tree = api.list_repo_tree(
            repo_id=HF_REPO,
            path=folder,
            recursive=False,
            repo_type="dataset",
        )
    except Exception as e:
        print(f"ERROR listing {folder}: {e}", file=sys.stderr)
        sys.exit(1)

    files = []
    for entry in tree:
        if entry.type != "file":
            continue
        # Only include files we expect to process
        if not entry.path.lower().endswith((".jsonl", ".parquet", ".csv")):
            continue
        files.append({"path": entry.path, "sha": entry.lfs.get("oid", "")})

    out = {
        "date": args.date,
        "folder": folder,
        "files": files,
    }
    json.dump(out, sys.stdout, indent=2)

if __name__ == "__main__":
    main()