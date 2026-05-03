#!/usr/bin/env python3
"""
Single non-recursive HF API call to list files for a date folder.
Usage:
  python tools/build_filelist.py --repo axentx/surrogate-1-training-pairs --date 2026-04-29 > file-list.json
"""
import argparse
import json
import sys

from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser(description="List repo tree non-recursively for a date folder.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Date folder (e.g. 2026-04-29)")
    parser.add_argument("--out", default=None, help="Optional output file (default: stdout)")
    args = parser.parse_args()

    api = HfApi()
    try:
        entries = api.list_repo_tree(
            repo_id=args.repo,
            path=args.date,
            recursive=False,
            repo_type="dataset",
        )
    except Exception as exc:
        print(f"ERROR: failed to list repo tree: {exc}", file=sys.stderr)
        sys.exit(1)

    files = sorted([e.path for e in entries if e.type == "file"])
    payload = {"date": args.date, "repo": args.repo, "files": files}

    out_f = open(args.out, "w") if args.out else sys.stdout
    try:
        json.dump(payload, out_f, indent=2)
        out_f.write("\n")
    finally:
        if args.out:
            out_f.close()

if __name__ == "__main__":
    main()