#!/usr/bin/env python3
"""
Create a deterministic snapshot of public dataset files for one date folder.
Usage:
  python list_files.py --repo axentx/surrogate-1-training-pairs \
                       --date 2026-05-02 \
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
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", default="file_list.json")
    args = parser.parse_args()

    api = HfApi()
    folder = args.date
    try:
        # Non-recursive to avoid 100× pagination bursts
        tree = api.list_repo_tree(repo_id=args.repo, path=folder, recursive=False)
    except Exception as exc:
        print(f"ERROR listing {args.repo}/{folder}: {exc}", file=sys.stderr)
        sys.exit(1)

    files = sorted([f.rfilename for f in tree if f.type == "file"])
    payload = {
        "date": folder,
        "snapshot_ts": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()