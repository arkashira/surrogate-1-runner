#!/usr/bin/env python3
"""
Single HF API call to list files for a date folder.

Usage:
  HF_TOKEN=<token> python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json

Produces:
[
  {"path": "batches/public-merged/2026-05-02/shard0-120000.jsonl", "size": 12345, "sha256": "..."},
  ...
]
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token)

    folder = f"batches/public-merged/{args.date}"
    entries = api.list_repo_tree(repo_id=args.repo, path=folder, recursive=True)

    files = []
    for e in entries:
        if getattr(e, "type", None) != "file":
            continue
        path = getattr(e, "path", None)
        if not path:
            continue
        size = getattr(e, "size", None)
        sha256 = getattr(e, "lfs", {}).get("sha256", None) if getattr(e, "lfs", None) else None
        files.append({"path": path, "size": size or 0, "sha256": sha256})

    # Deterministic ordering for stable shard assignment
    files.sort(key=lambda x: x["path"])

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(files, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")


if __name__ == "__main__":
    main()