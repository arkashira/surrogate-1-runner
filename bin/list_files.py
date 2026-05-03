#!/usr/bin/env python3
"""
Usage (Mac, after rate-limit window clears):
  python bin/list_files.py --repo axentx/surrogate-1-training-pairs --date 2026-05-02 --out file-list-2026-05-02.json

Produces:
  {
    "date": "2026-05-02",
    "files": [
      "public-merged/2026-05-02/file1.parquet",
      "batches/mirror-merged/2026-05-02/file2.parquet",
      ...
    ]
  }
"""
import argparse
import json
import sys
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    api = HfApi()
    prefixes = [
        f"public-merged/{args.date}",
        f"batches/mirror-merged/{args.date}",
    ]

    files = []
    for prefix in prefixes:
        try:
            items = api.list_repo_tree(repo_id=args.repo, path=prefix, recursive=False)
            for item in items:
                if item.rfilename.endswith((".jsonl", ".parquet")):
                    files.append(f"{prefix}/{item.rfilename}")
        except Exception as e:
            print(f"WARN: {prefix} -> {e}", file=sys.stderr)

    manifest = {"date": args.date, "files": sorted(files)}
    with open(args.out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()