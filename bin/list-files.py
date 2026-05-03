#!/usr/bin/env python3
"""
Usage:
  python bin/list-files.py <repo> <date_folder> > file-list.json

Example:
  python bin/list-files.py axentx/surrogate-1-training-pairs 2026-05-02 > file-list.json

Outputs newline-delimited JSON:
  {"path":"batches/public-merged/2026-05-02/shard-0-143000.parquet","size":12345,"sha256":"..."}
"""

import hashlib
import json
import os
import sys
from huggingface_hub import HfApi

def main():
    if len(sys.argv) != 3:
        print("Usage: list-files.py <repo> <date_folder>", file=sys.stderr)
        sys.exit(1)

    repo_id = sys.argv[1]
    date_folder = sys.argv[2].lstrip("/")
    api = HfApi(token=os.getenv("HF_TOKEN"))

    # Non-recursive per-folder to avoid pagination on big repos
    entries = api.list_repo_tree(repo_id=repo_id, path=date_folder, recursive=False)

    out = []
    for entry in entries:
        if entry.type != "file":
            continue
        out.append({
            "path": f"{date_folder}/{entry.path.split('/')[-1]}",
            "size": getattr(entry, "size", None),
            "sha256": getattr(entry, "lfs", {}).get("oid", "").replace("sha256:", "")
                    if getattr(entry, "lfs", None) else None,
        })

    for item in out:
        print(json.dumps(item, ensure_ascii=False))

if __name__ == "__main__":
    main()