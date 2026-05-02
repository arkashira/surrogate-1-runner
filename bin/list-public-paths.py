#!/usr/bin/env python3
"""
Generate CDN file-list for a date folder in axentx/surrogate-1-training-pairs.
Usage:
  python list-public-paths.py 2026-05-03 > file-list-2026-05-03.json
"""
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

REPO = "datasets/axentx/surrogate-1-training-pairs"

def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.utcnow().strftime("%Y-%m-%d")
    # Expect folder layout: public-raw/YYYY/MM/DD/  (adjust if different)
    folder = f"public-raw/{date_str.replace('-', '/')}"
    api = HfApi(token=os.getenv("HF_TOKEN"))

    entries = api.list_repo_tree(repo_id=REPO, path=folder, recursive=False)
    files = []
    for e in entries:
        if getattr(e, "type", None) != "file":
            continue
        # CDN URL (no auth, bypasses API rate limits)
        cdn_url = f"https://huggingface.co/datasets/{REPO}/resolve/main/{e.path}"
        files.append({"path": e.path, "cdn_url": cdn_url, "size": getattr(e, "size", None)})

    payload = {"date": date_str, "folder": folder, "files": files}
    sys.stdout.write(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()