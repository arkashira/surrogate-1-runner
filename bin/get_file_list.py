#!/usr/bin/env python3
"""
Generate file-list.json for a date folder in axentx/surrogate-1-training-pairs.
Run on Mac (or any machine with HF token) to avoid list_repo_files recursion.

Usage:
  HF_TOKEN=hf_xxx python bin/get_file_list.py --date 2026-05-03 --out file-list.json
"""

import argparse
import json
import os
from huggingface_hub import HfApi

API = HfApi()
REPO = "datasets/axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-03")
    parser.add_argument("--out", default="file-list.json")
    args = parser.parse_args()

    # Non-recursive per folder to avoid pagination explosion
    folder = f"batches/public-raw/{args.date}"
    items = API.list_repo_tree(repo_id=REPO, path=folder, recursive=False)

    # Flatten only files (ignore subfolders)
    files = [it.rfilename for it in items if not it.rfilename.endswith("/")]

    # Save manifest for workers
    payload = {
        "date": args.date,
        "folder": folder,
        "files": sorted(files),
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()