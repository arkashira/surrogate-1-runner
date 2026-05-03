#!/usr/bin/env python3
"""
Usage:
  python scripts/build_file_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --out manifest-2026-05-03.json

Produces manifest with CDN URLs and byte sizes.
Run once per date folder after rate-limit window clears.
"""
import argparse
import json
import os
import time
from huggingface_hub import HfApi

HF_API = HfApi()
CDN_TMPL = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def build_manifest(repo: str, date: str, out_path: str):
    folder = f"batches/public-merged/{date}"
    print(f"Listing {repo}/{folder} ...")
    entries = HF_API.list_repo_tree(repo=repo, path=folder, recursive=False)

    files = []
    for e in entries:
        if getattr(e, "type", None) != "file":
            continue
        if not getattr(e, "path", "").endswith((".jsonl", ".parquet")):
            continue
        cdn_url = CDN_TMPL.format(repo=repo, path=e.path)
        files.append({
            "path": e.path,
            "cdn_url": cdn_url,
            "size": getattr(e, "size", None),
        })

    files.sort(key=lambda x: x["path"])

    manifest = {
        "repo": repo,
        "date": date,
        "folder": folder,
        "created_ts": int(time.time()),
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {len(files)} files -> {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()
    build_manifest(args.repo, args.date, args.out)