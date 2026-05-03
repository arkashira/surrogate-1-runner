#!/usr/bin/env python3
"""
Generate a flat manifest for a date folder to avoid recursive HF API calls.
Usage:
  HF_TOKEN=... python bin/gen-manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --out manifest-2026-05-03.json
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi, list_repo_tree

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under public-merged/ or raw/")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--prefix", default="public-raw", help="Top-level folder in repo")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token) if token else HfApi()

    # List only one level at a time to avoid huge recursive pagination.
    # We assume date folder contains only files (or shallow subfolders).
    base = f"{args.prefix}/{args.date}"
    entries = list_repo_tree(repo_id=args.repo, path=base, recursive=False)

    files = []
    for e in entries:
        if e.type == "file":
            files.append(e.path)
        elif e.type == "dir":
            # shallow list inside subfolder (avoid deep recursion)
            sub = list_repo_tree(repo_id=args.repo, path=e.path, recursive=False)
            for se in sub:
                if se.type == "file":
                    files.append(se.path)

    manifest = {
        "repo": args.repo,
        "date": args.date,
        "prefix": args.prefix,
        "files": sorted(files),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()