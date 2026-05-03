#!/usr/bin/env python3
"""
Usage (Mac, after rate-limit window clears):
  python3 bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --path batches/public-merged/2026-05-02 \
    --out file-list.json

Output:
{
  "repo": "...",
  "path": "...",
  "files": [
    {"path": "batches/public-merged/2026-05-02/shard0-120000.jsonl", "size": 12345},
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    api = HfApi()
    tree = api.list_repo_tree(repo_id=args.repo, path=args.path, recursive=False)
    files = [{"path": f.path, "size": f.size} for f in tree if f.type == "file"]

    payload = {
        "repo": args.repo,
        "path": args.path,
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()