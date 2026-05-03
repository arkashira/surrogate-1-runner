#!/usr/bin/env python3
"""
Snapshot one date folder from axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json

Outputs JSON list:
[
  {"path": "batches/public-merged/2026-05-02/shard0-123456.jsonl", "size": 12345, "sha256": "..."},
  ...
]
"""

import argparse
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi

REPO_DEFAULT = "axentx/surrogate-1-training-pairs"

def list_date_folder(repo_id: str, date: str) -> List[Dict]:
    api = HfApi(token=os.getenv("HF_TOKEN"))
    # non-recursive per-folder to avoid heavy pagination
    tree = api.list_repo_tree(
        repo_id=repo_id,
        path=f"batches/public-merged/{date}",
        recursive=False,
    )
    out = []
    for entry in tree:
        if entry.type != "file":
            continue
        out.append({
            "path": f"batches/public-merged/{date}/{entry.path}",
            "size": getattr(entry, "size", None),
            "sha256": getattr(entry, "lfs", {}).get("oid", None) if hasattr(entry, "lfs") else None,
        })
    return out

def main() -> None:
    parser = argparse.ArgumentParser(description="Snapshot date folder file list.")
    parser.add_argument("--repo", default=REPO_DEFAULT, help="HF dataset repo id")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under batches/public-merged/")
    parser.add_argument("--out", default="file-list.json", help="Output JSON path")
    args = parser.parse_args()

    if not os.getenv("HF_TOKEN"):
        print("ERROR: HF_TOKEN env var required", file=sys.stderr)
        sys.exit(1)

    try:
        items = list_date_folder(args.repo, args.date)
    except Exception as exc:
        print(f"ERROR: failed to list folder: {exc}", file=sys.stderr)
        sys.exit(1)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"Wrote {len(items)} entries to {args.out}")

if __name__ == "__main__":
    main()