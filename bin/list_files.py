#!/usr/bin/env python3
"""
Produce file_list.json for a single date folder.
Run from Mac (or once per cron tick) after rate-limit window clears.

Usage:
  python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --path batches/public-merged/2026-05-02 \
    --out file_list.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    api = HfApi()
    # recursive=False avoids 100x pagination on big repos
    tree = api.list_repo_tree(repo_id=args.repo, path=args.path, recursive=False)
    files = [
        {
            "path": node.path,
            "cdn_url": f"https://huggingface.co/datasets/{args.repo}/resolve/main/{node.path}"
        }
        for node in tree
        if not node.path.endswith("/")
    ]

    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    payload = {
        "repo": args.repo,
        "path": args.path,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(files),
        "files": files
    }
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {out_path}")

if __name__ == "__main__":
    main()