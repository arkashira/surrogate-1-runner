#!/usr/bin/env python3
"""
Generate deterministic file-list for a date folder in axentx/surrogate-1-training-pairs.
Usage:
  python bin/list-files.py --date 2026-05-02 --out file-list.json
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

REPO_ID = "datasets/axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", default="file-list.json", help="Output JSON path")
    parser.add_argument("--token", default=os.getenv("HF_TOKEN"), help="HF token (optional for public reads)")
    args = parser.parse_args()

    api = HfApi(token=args.token)
    folder = f"{args.date}"
    print(f"Listing {REPO_ID}/{folder} ...", file=sys.stderr)

    # Non-recursive per top-level date folder; keeps API usage minimal.
    entries = api.list_repo_tree(repo_id=REPO_ID, path=folder, recursive=False)

    files = []
    for e in entries:
        if e.type != "file":
            continue
        # CDN URL (no auth required for public datasets)
        cdn_url = f"https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{folder}/{e.path}"
        files.append({
            "path": f"{folder}/{e.path}",
            "size": e.size,
            "lfs": getattr(e, "lfs", None),
            "cdn_url": cdn_url,
        })

    out = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "date": args.date,
        "repo": REPO_ID,
        "count": len(files),
        "files": files,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {len(files)} entries to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()