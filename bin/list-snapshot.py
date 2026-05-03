#!/usr/bin/env python3
"""
Generate deterministic file listing for surrogate-1 dataset.
Usage:
  HF_TOKEN=... python bin/list-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --out snapshot-20260503.json
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

from huggingface_hub import HfApi, Repository, hf_hub_download
from huggingface_hub.utils import HFValidationError

API = HfApi()

def list_snapshot(repo_id: str, out_path: str, date_folder: str = "") -> None:
    try:
        # Single API call: non-recursive tree per folder (avoids list_repo_files pagination)
        entries = API.list_repo_tree(repo_id=repo_id, path=date_folder, recursive=False)
    except Exception as e:
        if "429" in str(e):
            retry_after = 360
            print(f"HF API 429, retry after {retry_after}s", file=sys.stderr)
            time.sleep(retry_after)
            return list_snapshot(repo_id, out_path, date_folder)
        raise

    files = []
    for e in entries:
        if e.type != "file":
            continue
        path = e.path
        # CDN URL (no Authorization header required; bypasses /api/ rate limits)
        cdn_url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{path}"
        files.append({
            "path": path,
            "size": getattr(e, "size", None),
            "sha": getattr(e, "sha", None),
            "cdn_url": cdn_url,
        })

    snapshot = {
        "repo_id": repo_id,
        "date_folder": date_folder or "root",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Wrote {len(files)} files to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate CDN snapshot for surrogate-1 dataset")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--date-folder", default="", help="Optional date subfolder (e.g. batches/public-merged/20260503)")
    args = parser.parse_args()

    if "HF_TOKEN" not in os.environ:
        print("WARNING: HF_TOKEN not set — listing public repo only", file=sys.stderr)

    list_snapshot(args.repo, args.out, args.date_folder)