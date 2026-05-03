#!/usr/bin/env python3
"""
Usage (Mac orchestration):
  python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file_list.json

Produces:
  {
    "repo": "...",
    "date": "...",
    "files": [
      "batches/public-merged/2026-05-02/file1.parquet",
      ...
    ],
    "cdn_prefix": "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/"
  }
"""

import argparse
import json
import os
import sys
from typing import List

try:
    from huggingface_hub import HfApi
except ImportError:
    print("error: huggingface_hub not installed", file=sys.stderr)
    sys.exit(1)

CDN_PREFIX = "https://huggingface.co/datasets/{repo}/resolve/main/"

def list_date_files(repo: str, date: str) -> List[str]:
    api = HfApi()
    folder = f"batches/public-merged/{date}"
    try:
        items = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    except Exception as exc:
        raise RuntimeError(f"HF list_repo_tree failed for {repo}/{folder}: {exc}") from exc

    files = []
    for item in items:
        if hasattr(item, "path") and item.path:
            # list_repo_tree may return nested objects; accept path string
            files.append(item.path)
    files.sort()
    return files

def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-flight file listing for CDN-only ingestion")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under batches/public-merged/")
    parser.add_argument("--out", default="file_list.json", help="Output JSON path")
    args = parser.parse_args()

    files = list_date_files(args.repo, args.date)
    payload = {
        "repo": args.repo,
        "date": args.date,
        "files": files,
        "cdn_prefix": CDN_PREFIX.format(repo=args.repo),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")

    print(f"listed {len(files)} files -> {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()