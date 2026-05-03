#!/usr/bin/env python3
"""
Generate manifest for one date folder.
Usage:
  python bin/manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --folder batches/public-raw/2026-05-03 \
    --out manifest.json
"""
import argparse
import json
import os
import sys
import time
from typing import List, Dict

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def list_folder_files(repo: str, folder: str) -> List[Dict]:
    api = HfApi()
    items = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    files = [i for i in items if i.type == "file"]
    out = []
    for f in files:
        out.append({
            "path": f.path,
            "cdn_url": CDN_TEMPLATE.format(repo=repo, path=f.path),
            "size": getattr(f, "size", None),
        })
    return out

def build_manifest(repo: str, folder: str, out_path: str) -> None:
    files = list_folder_files(repo, folder)
    if not files:
        print(f"No files in {repo}/{folder}", file=sys.stderr)
        sys.exit(1)

    manifest = {
        "repo": repo,
        "folder": folder,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": files,
    }
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"Manifest written to {out_path} ({len(files)} files)")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    p.add_argument("--folder", required=True)
    p.add_argument("--out", default="manifest.json")
    args = p.parse_args()
    build_manifest(args.repo, args.folder, args.out)