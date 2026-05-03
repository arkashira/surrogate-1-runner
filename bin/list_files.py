#!/usr/bin/env python3
"""
Generate deterministic file list + content hash for a date folder in
axentx/surrogate-1-training-pairs.

Usage (Mac orchestration):
  python3 bin/list_files.py --date 2026-05-02 --out file-list.json

Outputs JSON:
{
  "repo": "axentx/surrogate-1-training-pairs",
  "date": "2026-05-02",
  "files": [
    "batches/public-merged/2026-05-02/part-00000.parquet",
    ...
  ],
  "sha256": "e3b0c442...",
  "cdn_base": "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main"
}
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime

try:
    from huggingface_hub import HfApi
except ImportError:
    print("error: huggingface_hub not installed", file=sys.stderr)
    sys.exit(1)

API = HfApi()
REPO = "axentx/surrogate-1-training-pairs"

def list_date_folder(date_str: str):
    folder_path = f"batches/public-merged/{date_str}"
    try:
        items = API.list_repo_tree(repo_id=REPO, path=folder_path, recursive=False)
    except Exception as exc:
        print(f"error listing {folder_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    files = []
    for item in items:
        if getattr(item, "type", None) == "file" or (hasattr(item, "path") and item.path):
            files.append(item.path)

    # Deterministic ordering so all shards see same snapshot
    files.sort()
    return files

def main():
    parser = argparse.ArgumentParser(description="Generate CDN file list + hash for date folder.")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under batches/public-merged/")
    parser.add_argument("--out", default="file-list.json", help="Output JSON path")
    args = parser.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("error: --date must be YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    files = list_date_folder(args.date)
    payload_bytes = json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    sha256 = hashlib.sha256(payload_bytes).hexdigest()

    payload = {
        "repo": REPO,
        "date": args.date,
        "files": files,
        "sha256": sha256,
        "cdn_base": f"https://huggingface.co/datasets/{REPO}/resolve/main",
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)

    print(f"wrote {len(files)} files -> {args.out}")

if __name__ == "__main__":
    main()