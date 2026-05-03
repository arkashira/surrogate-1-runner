#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in the public dataset repo.
Run from Mac (or cron) after rate-limit window clears.

Usage:
  python bin/list-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json
"""

import argparse
import json
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under datasets/")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    api = HfApi()
    # Single non-recursive call per folder (avoids 100x pagination)
    folder = f"batches/public-merged/{args.date}"
    try:
        tree = api.list_repo_tree(repo_id=args.repo, path=folder, recursive=False)
    except Exception as e:
        print(f"HF API error: {e}", file=sys.stderr)
        sys.exit(1)

    files = sorted(
        {
            f.rfilename
            for f in tree
            if f.rfilename.endswith((".jsonl", ".parquet"))
        }
    )

    snapshot = {
        "repo": args.repo,
        "date": args.date,
        "folder": folder,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "count": len(files),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Wrote {len(files)} files -> {args.out}")

if __name__ == "__main__":
    main()