#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in
axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json

Notes:
- Uses list_repo_tree(path, recursive=False) per folder to avoid 429.
- CDN downloads (resolve/main) are NOT counted against API rate limits.
- Output is deterministic (sorted paths) so shards are reproducible.
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi, list_repo_tree

def main() -> None:
    parser = argparse.ArgumentParser(description="List HF dataset files for a date folder.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", default="file-list.json")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN environment variable required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)
    root_path = f"batches/public-merged/{args.date}"

    # Single non-recursive tree call for the date folder
    entries = list_repo_tree(
        repo_id=args.repo,
        path=root_path,
        repo_type="dataset",
        recursive=False,
    )

    files = sorted(
        e.rfilename
        for e in entries
        if e.type == "file" and e.rfilename.lower().endswith((".jsonl", ".parquet", ".json"))
    )

    payload = {
        "repo": args.repo,
        "date": args.date,
        "root_path": root_path,
        "files": files,
        "count": len(files),
    }

    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()