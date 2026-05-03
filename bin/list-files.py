#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in
axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/list-files.py --date 2026-05-02 > file-list.json

Output keys:
  - path: repo path
  - size: bytes
  - sha256: if available in tree
  - url: CDN URL (no auth)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

REPO_ID = "axentx/surrogate-1-training-pairs"

def list_date_folder(date_str: str, api: HfApi) -> list[dict]:
    path = date_str
    try:
        tree = api.list_repo_tree(
            repo_id=REPO_ID,
            path=path,
            recursive=True,
            repo_type="dataset",
        )
    except Exception as exc:
        sys.stderr.write(f"Failed to list {path}: {exc}\n")
        return []

    out = []
    for node in tree:
        if node.type != "file":
            continue
        out.append(
            {
                "path": node.path,
                "size": node.size or 0,
                "sha256": getattr(node, "oid", None),
                "url": f"https://huggingface.co/datasets/{REPO_ID}/resolve/main/{node.path}",
            }
        )
    return out

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token)

    files = list_date_folder(args.date, api)
    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": args.date,
        "repo": REPO_ID,
        "count": len(files),
        "files": files,
    }
    json.dump(meta, sys.stdout, indent=2)
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()