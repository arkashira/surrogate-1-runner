#!/usr/bin/env python3
"""
Generate deterministic file list for a single date folder.
Run from Mac (or any dev machine) after rate-limit window clears.

Usage:
  python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-04-30 \
    --out file-list.json

Output format:
{
  "repo": "...",
  "date": "...",
  "files": [
    {"path": "batches/public-raw/2026-04-30/foo.parquet", "size": 12345},
    ...
  ],
  "generated_at": "2026-04-30T12:34:56Z"
}
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

CDN_BASE = "https://huggingface.co/datasets"

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="List HF dataset folder (non-recursive).")
    p.add_argument("--repo", required=True, help="HF dataset repo (user/name)")
    p.add_argument("--date", required=True, help="Date folder, e.g. 2026-04-30")
    p.add_argument("--out", default="file-list.json", help="Output JSON path")
    p.add_argument("--prefix", help="Optional custom prefix (overrides date)")
    return p

def list_folder(repo: str, date: str, prefix: str | None = None) -> list[dict]:
    api = HfApi()
    folder = prefix or f"batches/public-raw/{date}"
    # recursive=False avoids paginating 100x and hitting 429
    tree = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    files = []
    for entry in tree:
        if entry.type != "file":
            continue
        files.append({
            "path": entry.path,
            "size": entry.size or 0,
            "cdn_url": f"{CDN_BASE}/{repo}/resolve/main/{entry.path}"
        })
    # Deterministic ordering for stable shard assignment
    files.sort(key=lambda x: x["path"])
    return files

def main() -> None:
    args = build_parser().parse_args()
    try:
        files = list_folder(args.repo, args.date, args.prefix)
    except Exception as exc:
        print(f"ERROR listing folder: {exc}", file=sys.stderr)
        sys.exit(1)

    payload = {
        "repo": args.repo,
        "date": args.date,
        "prefix": args.prefix,
        "files": files,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds")
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()