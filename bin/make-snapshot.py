#!/usr/bin/env python3
"""
Generate deterministic file-list snapshot for surrogate-1 dataset.
Usage:
  HF_TOKEN=<token> python bin/make-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --out snapshot/2026-05-03/file-list.json
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi, list_repo_tree

def stable_slug(filename: str) -> str:
    return os.path.splitext(os.path.basename(filename))[0]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder in dataset")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN")
    if not token:
        print("HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)
    root = args.date  # e.g. "2026-05-03"
    entries = list_repo_tree(
        repo_id=args.repo,
        path=root,
        recursive=False,
        repo_type="dataset",
    )

    files = []
    for e in entries:
        if e.type != "file":
            continue
        slug = stable_slug(e.path)
        files.append(
            {
                "repo": args.repo,
                "path": e.path,
                "sha": e.lfs.get("oid", None) if getattr(e, "lfs", None) else None,
                "size": e.size,
                "slug": slug,
            }
        )

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": args.repo,
        "date": args.date,
        "root": root,
        "count": len(files),
        "files": sorted(files, key=lambda x: x["path"]),
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()