#!/usr/bin/env python3
"""
Generate manifest for a date folder to avoid recursive HF API during ingestion.
Usage:
  HF_TOKEN=... python3 bin/manifest-gen.py --date 2026-05-03
"""
import argparse
import json
import os
from pathlib import Path
from huggingface_hub import HfApi

API = HfApi()
REPO = "datasets/axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--out-dir", default="manifest")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.date}.json"

    # Single non-recursive tree call per date folder
    tree = API.list_repo_tree(REPO, path=args.date, recursive=False)
    files = []
    for entry in tree:
        if entry.type == "file":
            files.append(entry.path)

    # Also include nested folders one level down (non-recursive per folder)
    nested = []
    for entry in tree:
        if entry.type == "dir":
            sub = API.list_repo_tree(REPO, path=entry.path, recursive=False)
            for se in sub:
                if se.type == "file":
                    nested.append(se.path)

    all_files = sorted(set(files + nested))
    manifest = {
        "date": args.date,
        "repo": REPO,
        "files": all_files,
    }

    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(all_files)} files to {out_path}")

if __name__ == "__main__":
    main()