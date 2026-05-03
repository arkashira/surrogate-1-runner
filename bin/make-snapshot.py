#!/usr/bin/env python3
"""
Generate a deterministic snapshot for a date folder in
axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/make-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out snapshot-2026-05-02.json
"""

import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

HF_API = HfApi(token=os.getenv("HF_TOKEN"))

def list_date_folder(repo: str, date: str):
    """
    Single API call: list top-level folder contents non-recursively.
    Assumes layout: <date>/<slug>.parquet  (or other extensions).
    """
    prefix = f"{date}/"
    entries = HF_API.list_repo_tree(
        repo=repo,
        path=prefix,
        recursive=False,
    )
    # entries may include nested folders if any; filter to files only
    files = [e for e in entries if e.type == "file"]
    return files

def build_snapshot(repo: str, date: str):
    files = list_date_folder(repo, date)
    snapshot = {
        "repo": repo,
        "date": date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": [
            {
                "path": f.rfilename,  # relative path from repo root
                "size": f.size,
                "sha": getattr(f, "sha", None),
            }
            for f in files
        ],
    }
    return snapshot

def main():
    parser = argparse.ArgumentParser(description="Create CDN snapshot for date folder")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    if not os.getenv("HF_TOKEN"):
        print("error: HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    snapshot = build_snapshot(args.repo, args.date)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2)
    print(f"wrote {len(snapshot['files'])} files -> {args.out}")

if __name__ == "__main__":
    main()