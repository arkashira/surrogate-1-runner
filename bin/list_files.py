#!/usr/bin/env python3
"""
List files in a date folder of axentx/surrogate-1-training-pairs
and emit a JSON payload for CDN-only ingestion.

Usage:
  python bin/list_files.py --date 2026-05-02 --out file-list.json
"""
import argparse
import json
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

REPO = "axentx/surrogate-1-training-pairs"

def list_date_folder(date_str: str, out_path: str) -> None:
    api = HfApi()
    prefix = f"batches/public-merged/{date_str}/"
    items = api.list_repo_tree(repo_id=REPO, path=prefix, recursive=False)

    files = []
    for item in items:
        if item.type == "file":
            files.append({"path": item.path, "size": item.size})

    files.sort(key=lambda x: x["path"])

    payload = {
        "repo": REPO,
        "date": date_str,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)

    print(f"Wrote {len(files)} files to {out_path}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List files for a date folder.")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--out", default="file-list.json")
    args = parser.parse_args()

    try:
        list_date_folder(args.date, args.out)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)