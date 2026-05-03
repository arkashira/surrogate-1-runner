#!/usr/bin/env python3
"""
Generate a non-recursive file manifest for a date folder in axentx/surrogate-1-training-pairs.
Usage:
  HF_TOKEN=<token> python bin/build-manifest.py --repo axentx/surrogate-1-training-pairs \
    --folder batches/public-merged/2026-05-03 --out manifest-2026-05-03.json
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from huggingface_hub import HfApi, login

HF_API_RATE_LIMIT_RETRY = 360  # seconds (per pattern)
MAX_RETRIES = 5

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--folder", required=True, help="Folder path in repo (e.g. batches/public-merged/2026-05-03)")
    parser.add_argument("--out", required=True, help="Output JSON file")
    parser.add_argument("--token", default=os.getenv("HF_TOKEN"))
    args = parser.parse_args()

    if args.token:
        login(args.token)

    api = HfApi()
    folder = args.folder.rstrip("/")
    for attempt in range(MAX_RETRIES):
        try:
            entries = api.list_repo_tree(repo_id=args.repo, path=folder, recursive=False)
            break
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                print(f"Failed to list repo tree after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
                sys.exit(1)
            wait = HF_API_RATE_LIMIT_RETRY if "429" in str(e) else (2 ** attempt)
            print(f"Attempt {attempt+1} failed: {e}. Retry in {wait}s", file=sys.stderr)
            time.sleep(wait)

    files = []
    for entry in entries:
        path = getattr(entry, "path", entry.get("path") if isinstance(entry, dict) else None)
        if not path:
            continue
        if path.endswith((".parquet", ".jsonl")):
            files.append(path)

    manifest = {
        "repo": args.repo,
        "folder": folder,
        "files": sorted(files),
        "cdn_prefix": f"https://huggingface.co/datasets/{args.repo}/resolve/main",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()