#!/usr/bin/env python3
"""
Generate a flat manifest for a repo/path to avoid recursive HF API calls
during ingestion.

Usage:
  HF_TOKEN=... python bin/manifest-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --path raw/2026-05-03 \
    --out manifest.json
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

from huggingface_hub import HfApi, login

RATE_LIMIT_WAIT = 360

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", default="")
    parser.add_argument("--out", default="manifest.json")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if token:
        login(token=token)

    api = HfApi()
    entries = []
    cursor = None

    while True:
        try:
            tree = api.list_repo_tree(
                repo_id=args.repo,
                path=args.path or None,
                recursive=False,
                cursor=cursor,
            )
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limited, waiting {RATE_LIMIT_WAIT}s", file=sys.stderr)
                time.sleep(RATE_LIMIT_WAIT)
                continue
            raise

        for item in tree:
            if item.rfilename.endswith((".jsonl", ".parquet", ".json")):
                entries.append(item.rfilename)

        cursor = tree.next_cursor
        if not cursor:
            break

    manifest = {
        "repo": args.repo,
        "path": args.path or "",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": sorted(set(entries)),
    }

    Path(args.out).write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(manifest['files'])} files to {args.out}")

if __name__ == "__main__":
    main()