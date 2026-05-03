#!/usr/bin/env python3
"""
Usage:
  python bin/list-files.py --repo axentx/surrogate-1-training-pairs \
                           --folder batches/public-merged/2026-05-02 \
                           --out file-list.json

Produces:
  {
    "repo": "...",
    "folder": "...",
    "files": [
      {"path": "...", "size": 12345, "sha": "...", "lfs": false},
      ...
    ]
  }
"""

import argparse
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser(description="List repo folder (non-recursive) for CDN ingest.")
    parser.add_argument("--repo", required=True, help="HF dataset repo, e.g. axentx/surrogate-1-training-pairs")
    parser.add_argument("--folder", required=True, help="Folder path in repo (trailing slash optional)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    api = HfApi()
    folder = args.folder.rstrip("/") + "/"

    try:
        entries = api.list_repo_tree(
            repo_id=args.repo,
            path=folder.rstrip("/"),
            repo_type="dataset",
            recursive=False,
        )
    except Exception as exc:
        print(f"ERROR listing {args.repo}@{folder}: {exc}", file=sys.stderr)
        sys.exit(1)

    files = [
        {
            "path": e.path,
            "size": getattr(e, "size", 0),
            "sha": getattr(e, "sha", ""),
            "lfs": getattr(e, "lfs", False),
        }
        for e in entries
        if getattr(e, "type", "file") == "file"
    ]

    payload = {
        "repo": args.repo,
        "folder": folder,
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()