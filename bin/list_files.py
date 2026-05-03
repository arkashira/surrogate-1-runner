#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in
axentx/surrogate-1-training-pairs.

Usage:
  python bin/list_files.py --date 2026-05-02 --out file-list.json

Output schema:
{
  "repo": "axentx/surrogate-1-training-pairs",
  "date": "2026-05-02",
  "generated_at": "2026-05-02T22:00:00Z",
  "files": [
    {"path": "batches/public-raw/2026-05-02/foo.parquet", "size": 12345, "sha256": null},
    ...
  ]
}
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

REPO = "axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser(description="List repo files for a date folder (non-recursive per folder).")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--token", default=os.getenv("HF_TOKEN"), help="HF token (optional for public repo listing)")
    args = parser.parse_args()

    api = HfApi(token=args.token)
    folder_path = f"batches/public-raw/{args.date}"

    try:
        entries = api.list_repo_tree(
            repo_id=REPO,
            path=folder_path,
            repo_type="dataset",
            recursive=False,
        )
    except Exception as e:
        print(f"ERROR listing {folder_path}: {e}", file=sys.stderr)
        sys.exit(1)

    files = []
    for entry in entries:
        if entry.type != "file":
            continue
        files.append({
            "path": entry.path,
            "size": getattr(entry, "size", None),
            "sha256": None,
        })

    # Deterministic ordering for stable sharding
    files.sort(key=lambda x: x["path"])

    payload = {
        "repo": REPO,
        "date": args.date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()