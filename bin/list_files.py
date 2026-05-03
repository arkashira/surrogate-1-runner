#!/usr/bin/env python3
"""
List files for a single date folder in axentx/surrogate-1-training-pairs
and emit a JSON file with CDN URLs for CDN-only ingestion.

Usage:
  python3 bin/list_files.py --date 2026-04-29 --out file_list.json

Notes:
- Uses list_repo_tree(path, recursive=False) per subfolder to avoid
  recursive pagination (100× limit risk).
- CDN URLs are public and bypass HF API auth/rate limits.
"""

import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

REPO_ID = "datasets/axentx/surrogate-1-training-pairs"
CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def list_date_files(date_str: str):
    """
    Return list of dict:
      {"path": "...", "cdn_url": "...", "size": int|None}
    for files under snapshots/{date_str}/ and public-merged/{date_str}/
    """
    api = HfApi()
    date_str = date_str.strip("/")
    prefixes = [
        f"snapshots/{date_str}",
        f"public-merged/{date_str}",
        f"batches/public-merged/{date_str}",
    ]

    results = []
    seen = set()

    for prefix in prefixes:
        try:
            items = api.list_repo_tree(REPO_ID, path=prefix, recursive=False)
        except Exception as exc:
            # Path may not exist; skip silently
            print(f"Warning: could not list {prefix}: {exc}", file=sys.stderr)
            continue

        for item in items:
            # list_repo_tree may return nested tree objects; we only want files
            if getattr(item, "type", None) == "directory" or getattr(item, "size", None) is None:
                continue
            path = item.rfilename if hasattr(item, "rfilename") else str(item)
            if not path or path in seen:
                continue
            seen.add(path)
            cdn_url = CDN_TEMPLATE.format(repo=REPO_ID, path=path)
            results.append({
                "path": path,
                "cdn_url": cdn_url,
                "size": getattr(item, "size", None),
            })

    # Deterministic ordering for reproducible sharding
    results.sort(key=lambda x: x["path"])
    return results

def main():
    parser = argparse.ArgumentParser(description="List date folder files for CDN ingestion")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", default="file_list.json", help="Output JSON path")
    args = parser.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("Error: --date must be YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    files = list_date_files(args.date)
    payload = {
        "date": args.date,
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "repo": REPO_ID,
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) if os.path.dirname(args.out) else ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()