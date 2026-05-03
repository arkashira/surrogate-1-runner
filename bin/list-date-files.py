#!/usr/bin/env python3
"""
Generate a deterministic file list for a date folder.

Usage:
  HF_TOKEN=... \
  python bin/list-date-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date-folder 2026-05-02 \
    --out date-files.json
"""
import argparse
import json
import os
import time
from huggingface_hub import HfApi

HF_TOKEN = os.getenv("HF_TOKEN", "")

def list_date_files(repo_id: str, date_folder: str, out_path: str):
    api = HfApi(token=HF_TOKEN or None)
    # Single non-recursive call per date folder
    tree = api.list_repo_tree(repo_id=repo_id, path=date_folder, recursive=False)
    files = [{"path": f.rfilename, "size": f.size} for f in tree if f.type == "file"]

    payload = {
        "repo": repo_id,
        "date_folder": date_folder,
        "files": files,
        "listed_at_utc": int(time.time()),
    }

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {len(files)} files to {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--date-folder", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    list_date_files(args.repo, args.date_folder, args.out)