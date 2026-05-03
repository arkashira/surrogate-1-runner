#!/usr/bin/env python3
"""
Run on Mac after rate-limit window clears.
Usage:
  python bin/build-manifest.py --repo axentx/surrogate-1-training-pairs \
                               --date 2026-05-03 \
                               --out manifests/2026-05-03/files.json
"""
import argparse
import json
import os
from huggingface_hub import HfApi

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    api = HfApi(token=os.getenv("HF_TOKEN"))
    # Non-recursive: one folder = one date partition
    tree = api.list_repo_tree(repo_id=args.repo, path=args.date, recursive=False)

    files = []
    for item in tree:
        if item.type != "file":
            continue
        # CDN bypass: no auth header
        cdn_url = f"https://huggingface.co/datasets/{args.repo}/resolve/main/{args.date}/{item.path}"
        files.append({
            "path": item.path,
            "cdn_url": cdn_url,
            "size": getattr(item, "size", None)
        })

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(files, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()