#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in surrogate-1-training-pairs.
Run from Mac (or any dev machine) after rate-limit window clears.

Usage:
  python bin/list-date-files.py --repo axentx/surrogate-1-training-pairs --date 2026-05-02 --out file-list-2026-05-02.json
"""

import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def build_file_list(repo: str, date: str, out_path: str):
    api = HfApi()
    prefix = f"{date}/"
    try:
        tree = api.list_repo_tree(repo=repo, path=prefix, recursive=False)
    except Exception as exc:
        print(f"Error listing {repo}@{prefix}: {exc}", file=sys.stderr)
        sys.exit(1)

    entries = []
    for item in tree:
        if item.rfilename.endswith((".parquet", ".jsonl", ".json")):
            entries.append({
                "path": item.rfilename,
                "cdn_url": CDN_TEMPLATE.format(repo=repo, path=item.rfilename),
                "size": getattr(item, "size", None),
            })

    payload = {
        "repo": repo,
        "date": date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": sorted(entries, key=lambda x: x["path"]),
    }

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {len(entries)} entries to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List date folder files for CDN-only ingestion.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", default="file-list.json")
    args = parser.parse_args()
    build_file_list(repo=args.repo, date=args.date, out_path=args.out)