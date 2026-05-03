#!/usr/bin/env python3
"""
Download a single file from HuggingFace datasets CDN (no auth header).
Retries with exponential backoff.
"""
import argparse
import sys
import time
from pathlib import Path

import requests

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def download_cdn(repo: str, path: str, dest: Path, max_retries: int = 5) -> None:
    # Normalize path separators for HF CDN (always forward slash)
    path = path.replace("\\", "/").lstrip("/")
    url = CDN_TEMPLATE.format(repo=repo, path=path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        try:
            # No Authorization header -> bypasses /api/ rate limits
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return
        except Exception as exc:
            wait = 2 ** attempt
            print(f"Attempt {attempt}/{max_retries} failed for {path}: {exc}. Retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)

    raise RuntimeError(f"Failed to download {path} after {max_retries} attempts")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--dest", required=True, type=Path)
    args = parser.parse_args()
    download_cdn(args.repo, args.path, args.dest)