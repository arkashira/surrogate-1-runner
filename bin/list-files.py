#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-04-29 \
    --out file-list.json

Writes:
[
  {"path": "raw/abc/0000.parquet", "size": 12345, "sha256": "..."},
  ...
]
"""

import argparse
import hashlib
import json
import os
import sys
import time
from typing import List, Dict, Any

from huggingface_hub import HfApi

API = HfApi()

def list_date_folder(repo_id: str, date: str) -> List[Dict[str, Any]]:
    """List files in a date prefix non-recursively to avoid pagination storms."""
    prefix = f"{date}/"
    entries = API.list_repo_tree(repo_id, recursive=False, path=prefix)
    out = []
    for e in entries:
        if e.type != "file":
            continue
        out.append({
            "path": e.path,
            "size": e.size or 0,
            # sha256 not provided by tree; we'll skip or fetch via /resolve/ ETag if needed.
        })
    return out

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--out", default="file-list.json")
    args = parser.parse_args()

    # Be nice to API after 429: single call only.
    items = list_date_folder(args.repo, args.date)
    with open(args.out, "w") as f:
        json.dump(items, f, indent=2)
    print(f"Wrote {len(items)} files to {args.out}")

if __name__ == "__main__":
    main()