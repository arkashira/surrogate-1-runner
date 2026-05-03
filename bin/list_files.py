#!/usr/bin/env python3
"""
Usage (Mac, after rate-limit clears):
  python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --out file_list.json

Produces:
  {
    "repo": "...",
    "generated_at": "...",
    "folders": {
      "2026-04-29": ["file1.parquet", ...],
      ...
    },
    "cdn_base": "https://huggingface.co/datasets/{repo}/resolve/main"
  }
"""

import argparse
import json
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

CDN_TMPL = "https://huggingface.co/datasets/{repo}/resolve/main"

def list_date_folders(api: HfApi, repo: str):
    # Non-recursive top-level only (fast, 1 page)
    items = api.list_repo_tree(repo=repo, path="", recursive=False)
    folders = {}
    for item in items:
        if item.type == "directory":
            name = item.path.rstrip("/")
            # Expect YYYY-MM-DD; skip others
            if len(name) == 10 and name[4] == "-" and name[7] == "-":
                sub = api.list_repo_tree(repo=repo, path=name, recursive=False)
                files = [it.path for it in sub if it.type == "file"]
                folders[name] = sorted(files)
    return folders

def main():
    parser = argparse.ArgumentParser(description="List dataset files for CDN-only ingestion.")
    parser.add_argument("--repo", required=True, help="HF dataset repo (user/name)")
    parser.add_argument("--out", default="file_list.json", help="Output JSON path")
    args = parser.parse_args()

    api = HfApi()
    try:
        folders = list_date_folders(api, args.repo)
    except Exception as e:
        print(f"Error listing repo tree: {e}", file=sys.stderr)
        sys.exit(1)

    payload = {
        "repo": args.repo,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "folders": folders,
        "cdn_base": CDN_TMPL.format(repo=args.repo),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)

    print(f"Wrote {len(folders)} date folders to {args.out}")

if __name__ == "__main__":
    main()