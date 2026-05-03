#!/usr/bin/env python3
"""
Generate manifest.json for a date folder.
Run once per cron (Mac/CI) before workers start.
Usage:
  python bin/gen-manifest.py --repo axentx/surrogate-1-training-pairs --date 2026-05-03
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Folder name, e.g. 2026-05-03")
    parser.add_argument("--out", default="manifest.json")
    args = parser.parse_args()

    api = HfApi()
    # Single API call; recursive=False avoids pagination explosion.
    files = api.list_repo_tree(repo_id=args.repo, path=args.date, recursive=False)
    # Accept common training file patterns.
    paths = [f.rfilename for f in files if f.rfilename.endswith((".parquet", ".jsonl", ".json"))]

    manifest = {
        "repo": args.repo,
        "date": args.date,
        "files": sorted(paths),
        "cdn_prefix": f"https://huggingface.co/datasets/{args.repo}/resolve/main/{args.date}"
    }

    with open(args.out, "w", encoding="utf-8") as fp:
        json.dump(manifest, fp, indent=2)
    print(f"Wrote {len(paths)} files to {args.out}")

if __name__ == "__main__":
    main()