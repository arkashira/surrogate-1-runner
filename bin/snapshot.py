#!/usr/bin/env python3
"""
Produce a deterministic CDN manifest for a date folder in a HuggingFace dataset repo.

Usage:
  ./bin/snapshot.py --repo axentx/surrogate-1-training-pairs --date 2026-04-29 --out snapshot.json
"""

import argparse
import json
import sys
from pathlib import Path

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def main() -> None:
    parser = argparse.ArgumentParser(description="Create CDN snapshot for a dataset date folder.")
    parser.add_argument("--repo", required=True, help="HF dataset repo (e.g. axentx/surrogate-1-training-pairs)")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", default="snapshot.json", help="Output JSON path")
    args = parser.parse_args()

    api = HfApi()
    prefix = args.date.rstrip("/") + "/"
    entries = api.list_repo_tree(repo_id=args.repo, path=prefix, recursive=False)

    files = []
    for e in entries:
        if getattr(e, "type", None) == "file" or (hasattr(e, "path") and not e.path.endswith("/")):
            path = e.path
            files.append(
                {
                    "path": path,
                    "cdn_url": CDN_TEMPLATE.format(repo=args.repo, path=path),
                    "size": getattr(e, "size", 0),
                }
            )

    files.sort(key=lambda x: x["path"])

    out_path = Path(args.out)
    out_path.write_text(json.dumps(files, indent=2) + "\n")
    print(f"Wrote {len(files)} files to {out_path}", file=sys.stderr)

if __name__ == "__main__":
    main()