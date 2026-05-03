#!/usr/bin/env python3
"""
Generate manifest-{DATE}.json for a given DATE.

Usage:
  HF_TOKEN=hf_xxx \
  python bin/gen-manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --out manifest-2026-05-03.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

HF_API = "https://huggingface.co/api/datasets"

def list_repo_tree(repo: str, date: str, token: Optional[str] = None) -> list:
    """
    Return list of dicts: {"path": "...", "type": "file", "size": ...}
    for files under {date}/ in the repo.
    """
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{HF_API}/{repo}/tree/main"
    params = {"recursive": "true", "path": date}
    resp = requests.get(url, headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    tree = resp.json()
    return [item for item in tree if item.get("type") == "file"]

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate manifest for a DATE folder.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="DATE folder (YYYY-MM-DD)")
    parser.add_argument("--out", required=True, help="Output manifest JSON path")
    parser.add_argument("--hf-token", default=os.getenv("HF_TOKEN"))
    args = parser.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        sys.exit("Invalid DATE format; expected YYYY-MM-DD")

    token = args.hf_token
    items = list_repo_tree(args.repo, args.date, token)

    manifest = {
        "repo": args.repo,
        "date": args.date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": [{"path": item["path"], "size": item.get("size", 0)} for item in items],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest written to {out_path} ({len(items)} files)")

if __name__ == "__main__":
    main()