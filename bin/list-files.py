#!/usr/bin/env python3
"""
Generate deterministic file list for a HuggingFace dataset repo.
Usage:
  HF_TOKEN=<token> python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --path raw/2026-05-02 \
    --out file-list.json

Notes:
- Uses list_repo_tree(path, recursive=False) per folder to avoid 429.
- CDN download URLs are NOT rate-limited by /api/ endpoints.
- Output is stable (sorted) so training scripts can embed it.
"""
import argparse
import json
import os
import sys
import time
from typing import List, Dict

from huggingface_hub import HfApi, RepositoryTreeEntry

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def list_folder(api: HfApi, repo: str, folder: str) -> List[RepositoryTreeEntry]:
    """Single non-recursive call per folder."""
    target = folder if folder else "."
    try:
        entries = api.list_repo_tree(repo=repo, path=target, recursive=False)
    except Exception as exc:
        print(f"ERROR listing {repo}/{target}: {exc}", file=sys.stderr)
        raise
    return entries

def build_file_list(repo: str, root: str, api: HfApi) -> List[Dict]:
    """
    Walk root non-recursively by known subfolders (avoids recursive list_repo_files).
    If root contains nested folders, we expand one level only.
    """
    entries = list_folder(api, repo, root)
    files = []

    for entry in entries:
        if entry.type == "file":
            files.append(
                {
                    "path": entry.path,
                    "size": getattr(entry, "size", None),
                    "lfs": getattr(entry, "lfs", None),
                    "cdn_url": CDN_TEMPLATE.format(repo=repo, path=entry.path),
                }
            )
        elif entry.type == "folder":
            # One-level expansion to avoid heavy recursive calls
            sub_entries = list_folder(api, repo, entry.path)
            for sub in sub_entries:
                if sub.type == "file":
                    files.append(
                        {
                            "path": sub.path,
                            "size": getattr(sub, "size", None),
                            "lfs": getattr(sub, "lfs", None),
                            "cdn_url": CDN_TEMPLATE.format(repo=repo, path=sub.path),
                        }
                    )

    # Deterministic ordering
    files.sort(key=lambda x: x["path"])
    return files

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CDN file list for HF dataset repo.")
    parser.add_argument("--repo", required=True, help="HF dataset repo (user/repo)")
    parser.add_argument("--path", default="", help="Root folder inside repo")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--retry-wait", type=int, default=360, help="Wait seconds on 429")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token)

    for attempt in range(3):
        try:
            files = build_file_list(args.repo, args.path, api)
            break
        except Exception as exc:
            if attempt == 2:
                print(f"FAILED after retries: {exc}", file=sys.stderr)
                sys.exit(1)
            print(f"Retry {attempt+1}/3 after {args.retry_wait}s: {exc}", file=sys.stderr)
            time.sleep(args.retry_wait)

    out = {
        "repo": args.repo,
        "root": args.path,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print(f"Wrote {len(files)} files -> {args.out}")

if __name__ == "__main__":
    main()