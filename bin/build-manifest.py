#!/usr/bin/env python3
"""
Usage: python bin/build-manifest.py --date 2026-05-03 --out manifests/2026-05-03/file-list.json
"""
import argparse
import json
import os
from huggingface_hub import HfApi

API = HfApi()
REPO = "datasets/axentx/surrogate-1-training-pairs"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date folder in repo (e.g. 2026-05-03)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    # Non-recursive to avoid pagination explosion
    entries = API.list_repo_tree(REPO, path=args.date, recursive=False)
    files = [e.path for e in entries if e.type == "file"]

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"date": args.date, "files": files}, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()