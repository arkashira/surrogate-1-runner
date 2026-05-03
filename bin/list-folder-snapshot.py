#!/usr/bin/env python3
"""
Create a snapshot of files in one folder of a Hugging Face dataset repo.
Usage:
  HF_TOKEN=... python bin/list-folder-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --folder public/2026-05-03 \
    --out snapshot.json
"""
import argparse
import json
import sys
import time
from huggingface_hub import HfApi, RepositoryError

def main():
    parser = argparse.ArgumentParser(description="Snapshot folder files from HF repo.")
    parser.add_argument("--repo", required=True, help="Repo ID (e.g., axentx/...)")
    parser.add_argument("--folder", required=True, help="Folder path in repo")
    parser.add_argument("--out", default="snapshot.json", help="Output JSON path")
    parser.add_argument("--token", default=None, help="HF token (or use HF_TOKEN)")
    args = parser.parse_args()

    token = args.token or sys.argv[1] if len(sys.argv) > 1 else None
    api = HfApi(token=token)

    try:
        tree = api.list_repo_tree(args.repo, path=args.folder, recursive=False)
    except RepositoryError as e:
        # If rate-limited, suggest retry after 360s
        if "429" in str(e):
            print("Rate limited (429). Retry after 360s.", file=sys.stderr)
            sys.exit(1)
        raise

    files = [item.rfilename for item in tree if item.type == "file"]
    snapshot = {"files": files, "base": args.folder.rstrip("/")}

    with open(args.out, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Snapshot written to {args.out} ({len(files)} files)")

if __name__ == "__main__":
    main()