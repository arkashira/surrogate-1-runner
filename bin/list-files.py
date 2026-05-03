#!/usr/bin/env python3
"""
Usage:
  python bin/list-files.py axentx/surrogate-1-training-pairs \
    --folder batches/public-merged/2026-05-02 \
    --out file-list.json

Produces:
[
  {"repo": "axentx/surrogate-1-training-pairs",
   "path": "batches/public-merged/2026-05-02/foo.parquet",
   "sha": "abc...",
   "size": 123456}
]
"""

import argparse
import json
import os
import sys
import time

try:
    from huggingface_hub import HfApi
except ImportError:
    print("Install: pip install huggingface_hub", file=sys.stderr)
    sys.exit(1)

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", help="HF dataset repo (user/name)")
    parser.add_argument("--folder", required=True, help="Folder to list (e.g. batches/public-merged/2026-05-02)")
    parser.add_argument("--out", default="file-list.json", help="Output JSON path")
    parser.add_argument("--retries", type=int, default=3, help="API retries")
    parser.add_argument("--retry-delay", type=int, default=10, help="Delay between retries (s)")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token) if token else HfApi()

    for attempt in range(1, args.retries + 1):
        try:
            tree = api.list_repo_tree(repo_id=args.repo, path=args.folder, recursive=True)
            break
        except Exception as e:
            if attempt == args.retries:
                print(f"Failed after {args.retries} attempts: {e}", file=sys.stderr)
                sys.exit(1)
            print(f"Attempt {attempt}/{args.retries} failed: {e}. Retrying in {args.retry_delay}s...", file=sys.stderr)
            time.sleep(args.retry_delay)

    files = []
    for node in tree:
        if node.type != "file":
            continue
        files.append({
            "repo": args.repo,
            "path": node.path,
            "sha": getattr(node, "sha", None),
            "size": getattr(node, "size", None),
            "cdn_url": CDN_TEMPLATE.format(repo=args.repo, path=node.path),
        })

    payload = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "count": len(files),
        "files": files,
    }

    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} entries to {args.out}")

if __name__ == "__main__":
    main()