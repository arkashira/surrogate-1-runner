#!/usr/bin/env python3
"""
Generate deterministic file-list for a date folder in axentx/surrogate-1-training-pairs.
Run from Mac/CI (after rate-limit window) and commit file-list.json alongside training code.

Usage:
  python bin/list-files.py --repo axentx/surrogate-1-training-pairs --path batches/public-merged --out file-list.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN")
API = HfApi(token=HF_TOKEN)

def list_folder(repo_id: str, path: str):
    """
    Use list_repo_tree(recursive=False) per folder to avoid heavy pagination.
    Returns list[dict] with keys: path, size, sha256 (if available), lfs.
    """
    entries = []
    try:
        tree = API.list_repo_tree(repo_id=repo_id, path=path, recursive=False)
    except Exception as exc:
        print(f"ERROR listing {repo_id}/{path}: {exc}", file=sys.stderr)
        raise

    for entry in tree:
        entries.append({
            "path": entry.path,
            "size": getattr(entry, "size", None),
            "sha256": getattr(entry, "sha256", None),
            "lfs": getattr(entry, "lfs", None),
        })
    return entries

def build_file_list(repo_id: str, root: str):
    """
    Walk root/YYYY-MM-DD/* by listing each date folder once.
    """
    root_tree = API.list_repo_tree(repo_id=repo_id, path=root, recursive=False)
    date_folders = [e.path for e in root_tree if e.type == "directory"]

    out = {
        "repo_id": repo_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": root,
        "folders": {},
    }

    for folder in sorted(date_folders):
        print(f"Listing {folder}...")
        entries = list_folder(repo_id, folder)
        out["folders"][folder] = entries
        # Be nice to API between folder listings
        time.sleep(0.2)

    return out

def main():
    parser = argparse.ArgumentParser(description="Generate CDN file-list for surrogate-1 dataset.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--path", default="batches/public-merged")
    parser.add_argument("--out", default="file-list.json")
    args = parser.parse_args()

    file_list = build_file_list(args.repo, args.path)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(file_list, f, indent=2)
    print(f"Wrote {args.out} ({len(file_list['folders'])} folders)")

if __name__ == "__main__":
    main()