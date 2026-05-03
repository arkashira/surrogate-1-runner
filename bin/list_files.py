#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in surrogate-1-training-pairs.
Usage:
    python bin/list_files.py --date 2026-04-29 --out file-list-2026-04-29.json
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi

REPO_ID = "datasets/axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-04-29")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    api = HfApi(token=os.getenv("HF_TOKEN"))
    try:
        tree = api.list_repo_tree(
            repo_id=REPO_ID,
            path=args.date,
            repo_type="dataset",
            recursive=False,
        )
    except Exception as e:
        print(f"Failed to list {args.date}: {e}", file=sys.stderr)
        sys.exit(1)

    files = [entry.path for entry in tree if entry.type == "file"]
    files.sort()

    payload = {
        "date": args.date,
        "repo": REPO_ID,
        "files": files,
        "count": len(files),
    }

    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()