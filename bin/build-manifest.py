#!/usr/bin/env python3
"""
Build a CDN-only manifest for a date folder in axentx/surrogate-1-training-pairs.
Usage:
  HF_TOKEN=<token> python bin/build-manifest.py --repo axentx/surrogate-1-training-pairs --date 2026-05-03
"""
import argparse
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi

def build_manifest(repo: str, date_folder: str) -> List[Dict]:
    api = HfApi(token=os.environ.get("HF_TOKEN"))
    # List top-level items in the date folder (non-recursive)
    entries = api.list_repo_tree(repo=repo, path=date_folder, recursive=False)

    manifest = []
    for entry in entries:
        if getattr(entry, "type", None) != "file":
            continue
        # entry.path is like "2026-05-03/file1.parquet"
        manifest.append({
            "path": entry.path,
            "size": getattr(entry, "size", None),
            # Prefer stable content id; fallback to path
            "content_id": getattr(entry, "oid", None) or entry.path,
        })
    return manifest

def main() -> None:
    parser = argparse.ArgumentParser(description="Build CDN manifest for date folder")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", help="Output JSON file (default: manifest-{date}.json)")
    args = parser.parse_args()

    out_path = args.out or f"manifest-{args.date}.json"
    manifest = build_manifest(repo=args.repo, date_folder=args.date)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote {len(manifest)} entries to {out_path}")

    # Optional: commit manifest to repo (run in CI with write token)
    if os.environ.get("COMMIT_MANIFEST"):
        api = HfApi(token=os.environ["HF_TOKEN"])
        api.upload_file(
            path_or_fileobj=out_path,
            path_in_repo=f"manifests/{os.path.basename(out_path)}",
            repo_id=args.repo,
        )
        print(f"Committed manifest to repo: manifests/{os.path.basename(out_path)}")

if __name__ == "__main__":
    main()