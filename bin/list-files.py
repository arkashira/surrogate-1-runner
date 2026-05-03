#!/usr/bin/env python3
"""
List files in a single folder (non-recursive) for a HuggingFace dataset repo.
Usage:
  HF_TOKEN=<token> python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --path batches/public-merged/2026-05-02 \
    --output file-list.json
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser(description="List repo folder (non-recursive).")
    parser.add_argument("--repo", required=True, help="HF dataset repo (user/repo)")
    parser.add_argument("--path", required=True, help="Folder path in repo")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token)

    try:
        tree = api.list_repo_tree(
            repo_id=args.repo,
            path=args.path,
            repo_type="dataset",
            recursive=False,
        )
    except Exception as exc:
        print(f"ERROR listing repo tree: {exc}", file=sys.stderr)
        sys.exit(1)

    files = []
    for entry in tree:
        if entry.type == "file":
            files.append({
                "path": entry.path,
                "size": getattr(entry, "size", None),
                "sha256": getattr(entry, "sha256", None),
            })

    out = {
        "repo": args.repo,
        "path": args.path,
        "files": files,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {len(files)} files to {args.output}")

if __name__ == "__main__":
    main()