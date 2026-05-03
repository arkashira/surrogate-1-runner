#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in axentx/surrogate-1-training-pairs.
Usage:
  HF_TOKEN=<token> python bin/list-files.py --repo axentx/surrogate-1-training-pairs \
    --folder batches/public-merged/2026-05-02 --out file-list.json
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

def sha256_of_repo_file(api, repo_id, path):
    try:
        info = api.repo_info(repo_id=repo_id, repo_type="dataset", files_metadata=True)
        for f in info:
            if f.path == path and getattr(f, "sha256", None):
                return f.sha256
    except Exception:
        pass
    return None

def main() -> None:
    parser = argparse.ArgumentParser(description="List repo folder for CDN-only ingestion")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--folder", required=True, help="Folder path in repo (e.g. batches/public-merged/2026-05-02)")
    parser.add_argument("--out", default="file-list.json")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN env var required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)

    # Use recursive=False per folder to avoid 100x pagination on big repos.
    entries = api.list_repo_tree(repo_id=args.repo, path=args.folder, recursive=False)
    files = [e for e in entries if e.type == "file"]

    # Sort for deterministic ordering across runs.
    files.sort(key=lambda f: f.path)

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": args.repo,
        "folder": args.folder,
        "strategy": "cdn-only",
        "files": [
            {
                "path": f.path,
                "size": getattr(f, "size", None),
                "sha256": sha256_of_repo_file(api, args.repo, f.path) or "",
            }
            for f in files
        ],
    }

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()