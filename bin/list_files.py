#!/usr/bin/env python3
"""
List public dataset files for a given date folder (or latest) and emit JSON.
Intended to run once per cron cycle on a Mac (or CI) before shard workers start.

Usage:
  python bin/list_files.py --repo axentx/surrogate-1-training-pairs \
                           --date 2026-05-02 \
                           --out file-list-2026-05-02.json
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def list_date_files(repo: str, date_folder: str, api: HfApi):
    """
    List files under <date_folder>/ recursively (shallow per folder) to avoid
    massive recursive listing. Returns list of dicts with cdn_url and metadata.
    """
    base = date_folder.strip("/")
    try:
        tree = api.list_repo_tree(repo=repo, path=base, recursive=False)
    except Exception as e:
        print(f"HF API error listing {repo}/{base}: {e}", file=sys.stderr)
        return []

    entries = []
    for item in tree:
        if item.type != "file":
            continue
        cdn_url = CDN_TEMPLATE.format(repo=repo, path=item.path)
        entries.append({
            "path": item.path,
            "cdn_url": cdn_url,
            "size": getattr(item, "size", None),
            "lfs": getattr(item, "lfs", None) is not None,
        })
    return entries

def main():
    parser = argparse.ArgumentParser(description="List dataset files for CDN ingestion.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    parser.add_argument("--out", required=True, help="Output JSON file")
    args = parser.parse_args()

    api = HfApi()
    files = list_date_files(args.repo, args.date, api)

    payload = {
        "repo": args.repo,
        "date": args.date,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()