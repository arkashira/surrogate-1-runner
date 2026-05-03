#!/usr/bin/env python3
"""
Usage:
  HF_TOKEN=... python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --out file-list.json \
    [--folder batches/public-merged/2026-05-02]

Writes:
{
  "repo": "...",
  "folder": "...",
  "generated_at_utc": "...",
  "files": [
    {"path": "...", "size": 123, "sha256": "...", "cdn_url": "..."},
    ...
  ],
  "count": N
}
"""

import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi, RepositoryTreeEntry

CDN_BASE = "https://huggingface.co/datasets"

def list_folder(api: HfApi, repo: str, folder: str) -> list[dict]:
    entries = api.list_repo_tree(repo=repo, path=folder.rstrip("/"), recursive=False)
    out = []
    for e in entries:
        if isinstance(e, RepositoryTreeEntry) and e.type == "file":
            out.append({
                "path": e.path,
                "size": e.size or 0,
                "lfs": getattr(e, "lfs", None) is not None,
                "sha256": getattr(e, "sha256", None),
                "cdn_url": f"{CDN_BASE}/{repo}/resolve/main/{e.path}"
            })
    out.sort(key=lambda x: x["path"])
    return out

def main() -> None:
    parser = argparse.ArgumentParser(description="List dataset files for CDN ingestion")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--out", default="file-list.json")
    parser.add_argument("--folder", default="batches/public-merged")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN env var required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)
    folder = args.folder.rstrip("/")

    try:
        files = list_folder(api, args.repo, folder)
    except Exception as exc:
        print(f"ERROR listing repo tree: {exc}", file=sys.stderr)
        sys.exit(1)

    payload = {
        "repo": args.repo,
        "folder": folder,
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "files": files,
        "count": len(files),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()