#!/usr/bin/env python3
"""
Generate deterministic file list for a HuggingFace dataset repo.

Usage:
  HF_TOKEN=<token> python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-04-29 \
    --out filelist.json

Output schema:
  [{"repo": "...", "path": "...", "cdn_url": "..."}, ...]
"""
import argparse
import json
import os
import sys
import time
from typing import Dict, List

from huggingface_hub import HfApi, login, utils

CDN_BASE = "https://huggingface.co/datasets"

def is_retryable(exc: Exception) -> bool:
    return isinstance(exc, utils.RepositoryNotFoundError) is False and (
        "429" in str(exc) or "502" in str(exc) or "503" in str(exc) or "504" in str(exc)
    )

def list_date_files(repo: str, date: str, api: HfApi) -> List[Dict[str, str]]:
    """
    Walk repo/date/* using non-recursive tree calls to minimize 429 risk.
    Returns deterministic sorted list of dicts with repo+path+cdn_url.
    """
    root = date.strip("/")
    out: List[Dict[str, str]] = []

    try:
        top = api.list_repo_tree(repo=repo, path=root, recursive=False)
    except Exception as e:
        print(f"Cannot list {repo}/{root}: {e}", file=sys.stderr)
        return out

    for entry in top:
        if entry.type != "directory":
            continue
        subpath = f"{root}/{entry.path}"
        try:
            files = api.list_repo_tree(repo=repo, path=subpath, recursive=False)
        except Exception as e:
            print(f"Cannot list {repo}/{subpath}: {e}", file=sys.stderr)
            continue

        for f in files:
            if f.type != "file":
                continue
            full = f"{subpath}/{f.path}"
            out.append({
                "repo": repo,
                "path": full,
                "cdn_url": f"{CDN_BASE}/{repo}/resolve/main/{full}"
            })

    out.sort(key=lambda x: x["path"])
    return out

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CDN file list for dataset repo.")
    parser.add_argument("--repo", required=True, help="HF dataset repo (user/name)")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", default="filelist.json", help="Output JSON path")
    parser.add_argument("--retry-wait", type=int, default=360, help="Wait on 429/5xx (s)")
    parser.add_argument("--max-retries", type=int, default=3, help="Max retries on transient errors")
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN")
    if token:
        login(token=token, add_to_git_credential=False)

    api = HfApi()

    for attempt in range(1, args.max_retries + 1):
        try:
            items = list_date_files(args.repo, args.date, api)
            break
        except Exception as e:
            if is_retryable(e) and attempt < args.max_retries:
                print(f"Retryable error, waiting {args.retry_wait}s (attempt {attempt}/{args.max_retries}): {e}", file=sys.stderr)
                time.sleep(args.retry_wait)
                continue
            print(f"Failed to list files: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        sys.exit("Failed after retries.")

    with open(args.out, "w", encoding="utf-8") as fp:
        json.dump(items, fp, indent=2, ensure_ascii=False)

    print(f"Wrote {len(items)} files to {args.out}")

if __name__ == "__main__":
    main()