#!/usr/bin/env python3
"""
Usage:
  python bin/list-date-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out date-files.json

Lists files under a date folder (non-recursive per subfolder) and produces:
{
  "date": "2026-05-02",
  "repo": "axentx/surrogate-1-training-pairs",
  "folders": {
    "public-raw/2026-05-02": ["file1.parquet", ...],
    "batches/public-merged/2026-05-02": ["shard0-120000.jsonl", ...]
  },
  "files": [
    {"path": "public-raw/2026-05-02/file1.parquet", "size": 12345},
    ...
  ]
}
"""
import argparse
import json
import os
import sys

from huggingface_hub import HfApi

def list_date_files(repo_id: str, date: str, out_path: str):
    api = HfApi()
    prefix = f"{date}"
    entries = api.list_repo_tree(repo_id, path=prefix, recursive=False)

    folders = {}
    files = []

    for e in entries:
        if e.type == "directory":
            subpath = e.path
            try:
                subentries = api.list_repo_tree(repo_id, path=subpath, recursive=False)
            except Exception as ex:
                print(f"WARN: failed to list {subpath}: {ex}", file=sys.stderr)
                continue
            folders[subpath] = [se.path.split("/")[-1] for se in subentries if se.type == "file"]
            for se in subentries:
                if se.type == "file":
                    files.append({"path": se.path, "size": getattr(se, "size", None)})
        elif e.type == "file":
            files.append({"path": e.path, "size": getattr(e, "size", None)})

    payload = {
        "date": date,
        "repo": repo_id,
        "folders": folders,
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) if os.path.dirname(out_path) else ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {len(files)} file entries to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List files for a date folder.")
    parser.add_argument("--repo", required=True, help="HF dataset repo id")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()
    list_date_files(args.repo, args.date, args.out)