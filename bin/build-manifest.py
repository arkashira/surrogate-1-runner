#!/usr/bin/env python3
"""
Build a CDN-only manifest for surrogate-1 dataset ingestion.
Usage:
  python bin/build-manifest.py axentx/surrogate-1-training-pairs \
    --out manifest-2026-05-03.json \
    --date-folder 2026-05-03
"""
import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", help="HF dataset repo, e.g. axentx/surrogate-1-training-pairs")
    parser.add_argument("--out", required=True, help="Output manifest JSON path")
    parser.add_argument("--date-folder", help="Top-level date folder (e.g. 2026-05-03). If omitted, uses all top-level folders.")
    parser.add_argument("--pattern", default="*.parquet", help="File pattern to include (simple glob-style, applied client-side)")
    args = parser.parse_args()

    api = HfApi()
    # Single API call per folder (non-recursive)
    entries = api.list_repo_tree(
        repo_id=args.repo,
        path=args.date_folder or "",
        recursive=False,
        repo_type="dataset",
    )

    # If no date_folder provided, we only list top-level folders (non-recursive).
    # For simplicity this script expects a date folder; CI can loop over folders.
    files = [e for e in entries if e.rfilename.endswith(".parquet")]
    if not files:
        print("No parquet files found.", file=sys.stderr)
        sys.exit(1)

    manifest = {
        "repo": args.repo,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "date_folder": args.date_folder or "all",
        "files": [],
    }

    for f in files:
        cdn_url = CDN_TEMPLATE.format(repo=args.repo, path=f.rfilename)
        manifest["files"].append({
            "path": f.rfilename,
            "size": getattr(f, "size", None),
            "cdn_url": cdn_url,
        })

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) if os.path.dirname(args.out) else ".", exist_ok=True)
    with open(args.out, "w") as fp:
        json.dump(manifest, fp, indent=2)
    print(f"Wrote {len(manifest['files'])} files to {args.out}")

if __name__ == "__main__":
    main()