#!/usr/bin/env python3
"""
Generate a date-scoped manifest for surrogate-1 ingestion.
Usage (Mac orchestrator):
  HF_TOKEN=... python bin/gen-manifest.py \
    --repo axentx/some-public-raw \
    --date 2026-05-03 \
    --out manifests/2026-05-03.json
"""
import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi, login

def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--out", required=True)
    p.add_argument("--token", default=os.getenv("HF_TOKEN"))
    return p

def main():
    args = build_parser().parse_args()
    if not args.token:
        print("HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    login(token=args.token)
    api = HfApi()

    # List top-level date folder only (avoid recursive on big repos)
    prefix = f"raw/{args.date}/"
    entries = api.list_repo_tree(repo_id=args.repo, path=prefix, recursive=False)

    files = []
    for e in entries:
        if not e.path.endswith((".json", ".jsonl", ".parquet", ".csv")):
            continue
        files.append({
            "path": e.path,
            "cdn_url": f"https://huggingface.co/datasets/{args.repo}/resolve/main/{e.path}"
        })

    manifest = {
        "repo": args.repo,
        "date": args.date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": sorted(files, key=lambda x: x["path"])
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()