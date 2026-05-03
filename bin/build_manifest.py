#!/usr/bin/env python3
"""
Run on Mac (or any dev machine) after HF API rate-limit window clears.
Produces manifest.json for a single date folder.

Usage:
  HF_TOKEN=hf_xxx python bin/build_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-04-30 \
    --out manifest.json
"""
import argparse
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi, login

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="Folder under datasets, e.g. 2026-04-30")
    parser.add_argument("--out", default="manifest.json")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("HF_TOKEN required", file=sys.stderr)
        sys.exit(1)
    login(token=token)

    api = HfApi()
    folder = f"batches/public-merged/{args.date}"
    try:
        entries = api.list_repo_tree(repo_id=args.repo, path=folder, recursive=False)
    except Exception as e:
        print(f"Failed to list {args.repo}/{folder}: {e}", file=sys.stderr)
        sys.exit(1)

    files: List[Dict[str, str]] = []
    for entry in entries:
        if getattr(entry, "type", None) != "file":
            continue
        path = getattr(entry, "path", None)
        if not path or not path.endswith(".parquet"):
            continue
        cdn_url = f"https://huggingface.co/datasets/{args.repo}/resolve/main/{path}"
        files.append({"path": path, "cdn_url": cdn_url})

    manifest = {
        "repo": args.repo,
        "date": args.date,
        "files": files,
        "generated_by": "bin/build_manifest.py",
    }

    with open(args.out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()