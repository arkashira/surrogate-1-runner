#!/usr/bin/env python3
"""
List non-recursive file tree for a HF dataset folder.
Usage:
  HF_TOKEN=... python list_folder_tree.py --repo axentx/surrogate-1-training-pairs --path batches/raw/2026-05-03
Outputs JSON list of file paths to stdout.
"""
import argparse
import json
import os
from huggingface_hub import HfApi

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", required=True)
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN")
    api = HfApi(token=token)

    # non-recursive listing
    tree = api.list_repo_tree(
        repo_id=args.repo,
        path=args.path,
        repo_type="dataset",
        recursive=False
    )
    files = [item.path for item in tree if item.type == "file"]

    print(json.dumps(files, indent=2))

if __name__ == "__main__":
    main()