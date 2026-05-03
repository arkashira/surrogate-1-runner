#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in axentx/surrogate-1-training-pairs.
Run from Mac/CI after rate-limit window clears. Produces file-list.json for workers.

Usage:
  HF_TOKEN=hf_xxx python bin/list-files.py --date 2026-05-02 --out file-list.json
"""

import argparse
import hashlib
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi

REPO_ID = "axentx/surrogate-1-training-pairs"

def list_date_folder(date: str, api: HfApi) -> List[Dict]:
    """
    Use list_repo_tree per folder (non-recursive) to avoid 100x pagination.
    Returns list of dicts: {"path": "...", "size": int, "sha256": str|None}
    """
    prefix = f"batches/public-merged/{date}/"
    entries = api.list_repo_tree(
        repo_id=REPO_ID,
        path=prefix.rstrip("/"),
        repo_type="dataset",
        recursive=False,
    )

    files = []
    for entry in entries:
        if entry.type != "file":
            continue
        try:
            meta = api.get_paths_info(
                repo_id=REPO_ID,
                paths=[entry.path],
                repo_type="dataset",
            )
            info = meta[0] if meta else None
            size = getattr(info, "size", None)
        except Exception:
            size = None

        files.append({
            "path": entry.path,
            "size": size,
            "sha256": None,
        })

    files.sort(key=lambda x: x["path"])
    return files

def main() -> None:
    parser = argparse.ArgumentParser(description="List files for date folder (CDN ingest).")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", default="file-list.json", help="Output JSON path")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN env var required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)

    try:
        files = list_date_folder(args.date, api)
    except Exception as exc:
        print(f"ERROR listing folder: {exc}", file=sys.stderr)
        sys.exit(1)

    payload = {
        "repo": REPO_ID,
        "date": args.date,
        "generated_by": "bin/list-files.py",
        "files": files,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} entries to {args.out}")

if __name__ == "__main__":
    main()