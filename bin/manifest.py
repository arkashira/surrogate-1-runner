#!/usr/bin/env python3
"""
Generate manifest for a single date folder.
Usage:
  python bin/manifest.py --repo axentx/surrogate-1-training-pairs \
                         --date 2026-05-03 \
                         --out manifest.json
"""
import argparse
import json
import os
from huggingface_hub import HfApi

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Folder name, e.g. 2026-05-03")
    parser.add_argument("--out", default="manifest.json")
    args = parser.parse_args()

    api = HfApi(token=os.getenv("HF_TOKEN"))
    # Single non-recursive call
    files = api.list_repo_tree(
        repo_id=args.repo,
        path=args.date,
        repo_type="dataset",
        recursive=False,
    )

    manifest = {
        "repo": args.repo,
        "date": args.date,
        "files": [
            {"path": f.rfilename, "size": f.size}
            for f in files if f.size and f.rfilename
        ],
    }

    with open(args.out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {len(manifest['files'])} files to {args.out}")

if __name__ == "__main__":
    main()