#!/usr/bin/env python3
"""
Usage:
  python bin/list_files.py axentx/surrogate-1-training-pairs 2026-05-02 > file-list.json

Outputs:
  [
    {"path": "raw/2026-05-02/foo.parquet", "sha256": "..."},
    ...
  ]

Notes:
- Uses huggingface_hub list_repo_tree (non-recursive per folder) to avoid 429.
- Falls back to repo root listing if subpath missing.
- sha256 is repo file LFS pointer hash when available; otherwise None.
"""
import json
import sys
from pathlib import Path

from huggingface_hub import HfApi, list_repo_tree

API = HfApi()

def list_files(repo_id: str, subpath: str = "") -> list[dict]:
    try:
        items = list_repo_tree(repo_id=repo_id, path=subpath, recursive=False)
    except Exception:
        # If subpath invalid, list root
        items = list_repo_tree(repo_id=repo_id, path="", recursive=False)

    out = []
    for item in items:
        if item.type != "file":
            continue
        out.append({
            "path": str(Path(subpath) / item.path) if subpath else item.path,
            "sha256": getattr(item, "lfs", {}).get("sha256") if hasattr(item, "lfs") else None,
        })
    return out

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: list_files.py <repo_id> [subpath]", file=sys.stderr)
        sys.exit(1)
    repo_id = sys.argv[1]
    subpath = sys.argv[2] if len(sys.argv) > 2 else ""
    result = list_files(repo_id, subpath)
    json.dump(result, sys.stdout, indent=None, separators=(",", ":"))

if __name__ == "__main__":
    main()