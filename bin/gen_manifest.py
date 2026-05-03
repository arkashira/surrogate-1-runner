#!/usr/bin/env python3
"""
Generate manifest for a date folder to avoid HF API calls during shard runs.
Usage:
  HF_TOKEN=... python bin/gen_manifest.py 2024-06-01
Writes: batches/public-merged/2024-06-01/manifest.json
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

import requests

HF_REPO = os.getenv("HF_REPO", "axentx/surrogate-1-training-pairs")
HF_TOKEN = os.getenv("HF_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def list_date_folders():
    url = f"https://huggingface.co/api/datasets/{HF_REPO}/tree"
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code == 429:
        sys.exit("HF API 429 — retry later")
    r.raise_for_status()
    items = r.json()
    folders = [item["path"] for item in items if item["type"] == "directory"]
    folders = [f for f in folders if len(f.split("-")) == 3 and len(f) == 10]
    folders.sort()
    return folders

def list_parquet_files(date_folder: str):
    url = f"https://huggingface.co/api/datasets/{HF_REPO}/tree"
    r = requests.get(url, params={"path": date_folder}, headers=HEADERS, timeout=30)
    if r.status_code == 429:
        sys.exit("HF API 429 — retry later")
    r.raise_for_status()
    items = r.json()
    files = [
        {"path": item["path"], "size": item.get("size", 0)}
        for item in items
        if item["type"] == "file" and item["path"].endswith(".parquet")
    ]
    files.sort(key=lambda x: x["path"])
    return files

def main():
    if len(sys.argv) < 2:
        # default to latest
        folders = list_date_folders()
        if not folders:
            sys.exit("No date folders found")
        date_folder = folders[-1]
    else:
        date_folder = sys.argv[1]

    files = list_parquet_files(date_folder)
    out_dir = Path("batches/public-merged") / date_folder
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"date": date_folder, "files": files}
    out_path = out_dir / "manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest written to {out_path}")

if __name__ == "__main__":
    main()