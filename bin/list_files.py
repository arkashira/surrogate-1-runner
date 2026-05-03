#!/usr/bin/env python3
"""
Deterministic pre-flight file lister for axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/list_files.py \
    --date 2026-05-02 \
    --out file-list/2026-05-02.json

Output format (list of dicts):
[
  {"path": "batches/public-merged/2026-05-02/file1.parquet", "size": 12345},
  ...
]
"""

import argparse
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi

REPO = "axentx/surrogate-1-training-pairs"
CDN_BASE = f"https://huggingface.co/datasets/{REPO}/resolve/main"

def list_date_files(date: str) -> List[Dict[str, object]]:
    """
    List parquet/jsonl files for a single date folder non-recursively.
    """
    api = HfApi()
    prefix = f"batches/public-merged/{date}/"
    try:
        tree = api.list_repo_tree(
            repo_id=REPO,
            path=prefix,
            repo_type="dataset",
            recursive=False,
        )
    except Exception as exc:
        print(f"Error listing tree for {prefix}: {exc}", file=sys.stderr)
        return []

    entries = []
    for item in tree:
        rfn = item.rfilename
        if rfn.endswith((".parquet", ".jsonl")):
            entries.append({
                "path": rfn,
                "size": getattr(item, "size", None),
                "cdn_url": f"{CDN_BASE}/{rfn}",
            })
    entries.sort(key=lambda x: x["path"])
    return entries

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic file list for a date folder.")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", help="Output JSON path (default: file-list/<date>.json)")
    args = parser.parse_args()

    os.makedirs("file-list", exist_ok=True)
    out_path = args.out or f"file-list/{args.date}.json"

    files = list_date_files(args.date)
    payload = {
        "repo": REPO,
        "date": args.date,
        "cdn_base": CDN_BASE,
        "files": files,
    }

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    print(f"Wrote {len(files)} files to {out_path}")

if __name__ == "__main__":
    main()