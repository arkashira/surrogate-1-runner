#!/usr/bin/env python3
"""
Generate a file list manifest for a HuggingFace dataset repo.
Uses list_repo_tree (non-recursive per folder) to avoid 429 rate limits.
Outputs JSON lines: {"repo":"...","path":"...","cdn_url":"...","size":...}
"""
import json
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, list_repo_tree

def main():
    repo = os.getenv("HF_REPO", "datasets/axentx/surrogate-1-training-pairs")
    root = os.getenv("HF_PATH", "")
    out = Path(os.getenv("OUT", "snapshot/files.json"))
    token = os.getenv("HF_TOKEN")

    api = HfApi(token=token)
    out.parent.mkdir(parents=True, exist_ok=True)

    # If root is empty, list top-level folders (assume date folders)
    entries = list_repo_tree(repo=repo, path=root, repo_type="dataset", token=token)
    folders = [e for e in entries if e.type == "directory"]
    if not folders:
        folders = [type('', (), {'path': root})]  # single root

    results = []
    for folder in folders:
        folder_path = folder.path
        items = list_repo_tree(repo=repo, path=folder_path, repo_type="dataset", token=token)
        for item in items:
            if item.type != "file":
                continue
            if not item.path.endswith((".jsonl", ".parquet", ".json")):
                continue
            cdn_url = f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
            results.append({
                "repo": repo,
                "path": item.path,
                "cdn_url": cdn_url,
                "size": getattr(item, "size", None),
                "folder": folder_path,
            })

    out.write_text(json.dumps(results, indent=2))
    print(f"Wrote {len(results)} files to {out}", file=sys.stderr)

if __name__ == "__main__":
    main()