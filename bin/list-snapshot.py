#!/usr/bin/env python3
"""
Produce a deterministic file-list snapshot for one date folder.
Usage:
  HF_TOKEN=<token> python bin/list-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under datasets/")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)
    # Non-recursive: one API call, no pagination explosion
    path = f"batches/public-merged/{args.date}"
    try:
        entries = api.list_repo_tree(repo_id=args.repo, path=path, recursive=False)
    except Exception as e:
        print(f"list_repo_tree failed: {e}", file=sys.stderr)
        sys.exit(1)

    files = [e.path for e in entries if e.type == "file"]
    files.sort()  # deterministic ordering

    snapshot = {
        "repo": args.repo,
        "date": args.date,
        "path_prefix": path,
        "files": files,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()