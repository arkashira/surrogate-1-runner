#!/usr/bin/env python3
"""
Generate deterministic file-list for a date folder in axentx/surrogate-1-training-pairs.
Usage:
  HF_TOKEN=<token> python bin/list-files.py --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 --out file-list.json
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

def sha256_of_path(path: str, api: HfApi, repo: str) -> str | None:
    """Best-effort LFS/OID lookup; fallback to path hash if unavailable."""
    try:
        meta = api.get_paths_metadata(repo_id=repo, paths=[path], repo_type="dataset")
        if meta and meta[0] and getattr(meta[0], "lfs", None):
            return meta[0].lfs.get("oid", "").replace("sha256:", "")
    except Exception:
        pass
    # Deterministic fallback
    return hashlib.sha256(path.encode()).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under data/ or root")
    parser.add_argument("--out", default="file-list.json")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)

    prefix = args.date if args.date.endswith("/") else f"{args.date}/"
    try:
        entries = api.list_repo_tree(
            repo_id=args.repo,
            path=prefix,
            repo_type="dataset",
            recursive=False,
        )
    except Exception:
        # Fallback: try root-level listing if date folder not found
        entries = api.list_repo_tree(
            repo_id=args.repo,
            path="",
            repo_type="dataset",
            recursive=False,
        )
        entries = [e for e in entries if e.path.startswith(prefix)]

    files = []
    for e in entries:
        if e.type != "file":
            continue
        sha256 = sha256_of_path(e.path, api, args.repo)
        cdn_url = f"https://huggingface.co/datasets/{args.repo}/resolve/main/{e.path}"
        files.append(
            {
                "path": e.path,
                "size": e.size,
                "sha256": sha256,
                "cdn_url": cdn_url,
            }
        )

    payload = {
        "repo": args.repo,
        "date": args.date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": files,
    }

    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()