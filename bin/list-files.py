#!/usr/bin/env python3
"""
List public dataset files once and emit file-list.json with integrity metadata.
Usage:
  HF_TOKEN=... python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json
"""
import argparse
import hashlib
import json
import os
import sys
from huggingface_hub import HfApi, login

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192 * 16), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="Date folder under data/ (e.g. 2026-05-02)")
    parser.add_argument("--out", required=True)
    parser.add_argument("--token", default=os.getenv("HF_TOKEN"))
    parser.add_argument("--cache-dir", default=os.getenv("HF_HOME", os.path.expanduser("~/.cache/huggingface")))
    args = parser.parse_args()

    if not args.token:
        print("ERROR: HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    login(token=args.token)
    api = HfApi()

    # Non-recursive per folder to avoid 100x pagination and 429s
    prefix = f"data/{args.date}/"
    entries = api.list_repo_tree(repo_id=args.repo, path=prefix, recursive=False)

    files = []
    cache_root = os.path.join(args.cache_dir, "datasets", args.repo, "resolve", "main")
    os.makedirs(cache_root, exist_ok=True)

    for entry in entries:
        if entry.type != "file":
            continue
        # CDN URL (no auth, bypasses /api/ rate limit)
        cdn_url = f"https://huggingface.co/datasets/{args.repo}/resolve/main/{entry.path}"
        # Local cache path (hf_hub_download style)
        cache_path = os.path.join(cache_root, os.path.basename(entry.path))
        sha256 = None
        if os.path.exists(cache_path):
            sha256 = sha256_file(cache_path)
        files.append(
            {
                "path": entry.path,
                "cdn_url": cdn_url,
                "size": getattr(entry, "size", None),
                "sha256": sha256,
                "cache_path": cache_path,
            }
        )

    payload = {"repo": args.repo, "date": args.date, "files": files}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files -> {args.out}")

if __name__ == "__main__":
    main()