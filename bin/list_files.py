#!/usr/bin/env python3
"""
Generate deterministic CDN file list for a date folder.

Usage:
  HF_TOKEN=<token> python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out filelist/2026-05-02.json

Outputs JSON lines:
  {"path": "raw/2026-05-02/file1.parquet", "size": 12345, "etag": "abc...", "cdn_url": "https://huggingface.co/datasets/.../resolve/main/raw/2026-05-02/file1.parquet"}
"""

import argparse
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi

HF_API = HfApi()

def list_date_files(repo_id: str, date: str, folder_prefix: str = "raw") -> List[Dict[str, object]]:
    """
    List files under <folder_prefix>/<date>/ without recursion.
    Single API call per folder to minimize rate-limit pressure.
    """
    prefix = f"{folder_prefix}/{date}/"
    try:
        tree = HF_API.list_repo_tree(repo_id=repo_id, path=prefix, recursive=False)
    except Exception as exc:
        print(f"ERROR listing repo tree for {repo_id}/{prefix}: {exc}", file=sys.stderr)
        raise

    entries = []
    for item in tree:
        if getattr(item, "type", None) == "file":
            path = item.path
            entries.append({
                "path": path,
                "size": getattr(item, "size", None),
                "etag": getattr(item, "etag", None),
                "cdn_url": f"https://huggingface.co/datasets/{repo_id}/resolve/main/{path}"
            })
    return entries

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CDN-friendly file list.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder to list")
    parser.add_argument("--out", required=True, help="Output JSON file")
    parser.add_argument("--folder-prefix", default="raw", help="Top folder inside repo")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    entries = list_date_files(args.repo, args.date, args.folder_prefix)
    with open(args.out, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print(f"Wrote {len(entries)} entries to {args.out}")

if __name__ == "__main__":
    main()