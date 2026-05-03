#!/usr/bin/env python3
"""
List top-level files in a repo path (non-recursive) using huggingface_hub.
Usage:
  HF_TOKEN=... ./bin/hf_list_tree.py <owner> <repo> <path>

Outputs JSON list of objects:
  [{"path": "...", "size": ...}, ...]
"""
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: hf_list_tree.py <owner> <repo> <path>", file=sys.stderr)
        sys.exit(1)
    owner, repo, path = sys.argv[1], sys.argv[2], sys.argv[3]
    api = HfApi(token=os.environ.get("HF_TOKEN"))
    entries = api.list_repo_tree(
        repo=f"{owner}/{repo}",
        path=path,
        repo_type="dataset",
        recursive=False,
    )
    files = []
    seen = set()
    for e in entries:
        if e.type == "file":
            if e.path in seen:
                print(f"Duplicate path in listing: {e.path}", file=sys.stderr)
                sys.exit(1)
            seen.add(e.path)
            files.append({"path": e.path, "size": getattr(e, "size", None)})
    # Deterministic ordering
    files.sort(key=lambda x: x["path"])
    print(json.dumps(files, separators=(",", ":")))

if __name__ == "__main__":
    main()