#!/usr/bin/env python3
"""
Generate a deterministic snapshot of dataset files for a date folder.
Usage:
  python bin/lib/snapshot.py --repo datasets/axentx/surrogate-1-training-pairs --date 2026-04-29 --out snapshot-2026-04-29.json
"""
import argparse
import json
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi


def main() -> None:
    parser = argparse.ArgumentParser(description="Create HF dataset file snapshot for a date folder.")
    parser.add_argument("--repo", required=True, help="HF repo (e.g., datasets/owner/name)")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--subpath", default="", help="Optional subpath within date folder")
    args = parser.parse_args()

    api = HfApi()
    folder_path = args.date
    if args.subpath:
        folder_path = f"{folder_path}/{args.subpath}".rstrip("/")

    try:
        entries = api.list_repo_tree(repo_id=args.repo, path=folder_path, recursive=False)
    except Exception as exc:
        print(f"ERROR: failed to list repo tree {args.repo}@{folder_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    files = []
    for entry in entries:
        files.append({
            "path": entry.path,
            "type": getattr(entry, "type", "file"),
            "size": getattr(entry, "size", None),
            "lfs": getattr(entry, "lfs", None),
        })

    files.sort(key=lambda f: f["path"])

    snapshot = {
        "repo": args.repo,
        "folder": folder_path,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "count": len(files),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, sort_keys=True)

    print(f"Snapshot written to {args.out} ({len(files)} files)")


if __name__ == "__main__":
    main()