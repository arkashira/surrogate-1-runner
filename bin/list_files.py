#!/usr/bin/env python3
"""
Generate deterministic file list for a HF dataset repo/date folder.

Usage:
  python bin/list_files.py axentx/surrogate-1-training-pairs 2026-05-01 > file-list.json
  # or
  python bin/list_files.py --repo axentx/surrogate-1-training-pairs --date 2026-05-01 --out file-list.json
"""

import argparse
import json
import sys
from huggingface_hub import HfApi

def list_files(repo_id: str, date_folder: str) -> dict:
    api = HfApi()
    # Single API call, non-recursive to avoid pagination explosion
    tree = api.list_repo_tree(repo_id, path=date_folder, recursive=False)
    files = []
    for item in tree:
        if item.type == "file":
            files.append({
                "path": item.path,
                "size": getattr(item, "size", None),
                "lfs": getattr(item, "lfs", None),
            })

    return {
        "repo_id": repo_id,
        "folder": date_folder,
        "count": len(files),
        "files": files,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="List HF dataset files for one date folder")
    parser.add_argument("repo_id", nargs="?", help="HF repo id (e.g. axentx/surrogate-1-training-pairs)")
    parser.add_argument("date_folder", nargs="?", help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--repo", help="HF repo id (alternative)", default=None)
    parser.add_argument("--date", help="Date folder (alternative)", default=None)
    parser.add_argument("--out", help="Output file (default: stdout)", default=None)
    args = parser.parse_args()

    repo = args.repo_id or args.repo
    date = args.date_folder or args.date

    if not repo or not date:
        parser.print_help(sys.stderr)
        sys.exit(1)

    result = list_files(repo, date)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    else:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")

if __name__ == "__main__":
    main()