#!/usr/bin/env python3
"""
Usage (Mac, after rate-limit window clears):
  HF_TOKEN=... python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list-2026-05-02.json

Produces JSON:
{
  "repo": "...",
  "date": "...",
  "files": [
    {"path": "raw/abc/...", "cdn_url": "https://huggingface.co/datasets/.../resolve/main/...", "size": 1234, "sha": "..."},
    ...
  ]
}
"""
import argparse
import json
import os
import sys
import time

from huggingface_hub import HfApi, list_repo_tree

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="Folder under datasets to list, e.g. 2026-05-02")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    api = HfApi(token=os.getenv("HF_TOKEN"))
    prefix = f"{args.date}/"

    # Non-recursive per-folder listing to avoid 100x pagination on big repos
    entries = list_repo_tree(
        repo_id=args.repo,
        path=prefix,
        recursive=False,
        repo_type="dataset",
    )

    files = []
    for e in entries:
        if e.type != "file":
            continue
        files.append({
            "path": e.path,
            "cdn_url": CDN_TEMPLATE.format(repo=args.repo, path=e.path),
            "size": e.size,
            "sha": e.lfs.get("sha256", "") if e.lfs else "",
        })

    payload = {
        "repo": args.repo,
        "date": args.date,
        "files": files,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()