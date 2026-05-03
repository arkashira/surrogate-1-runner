#!/usr/bin/env python3
"""
Snapshot utilities for surrogate-1 dataset folders.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi, list_repo_tree

REPO = "axentx/surrogate-1-training-pairs"
SNAPSHOT_DIR = Path(__file__).parents[2] / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True, parents=True)

api = HfApi()

def list_date_folder(date: str):
    """
    List files in public-merged/{date}/ (non-recursive).
    Returns list of filenames (relative to repo root).
    """
    prefix = f"public-merged/{date}/"
    try:
        files = list_repo_tree(repo_id=REPO, path=prefix, repo_type="dataset", recursive=False)
    except Exception as e:
        raise RuntimeError(f"Failed to list repo tree for {prefix}: {e}") from e
    # items are dicts with 'path'
    paths = [item["path"] for item in files if item.get("type") == "file"]
    return sorted(paths)

def save_snapshot(date: str, files):
    snapshot = {
        "repo": REPO,
        "date": date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }
    out = SNAPSHOT_DIR / f"public-merged-{date}.json"
    out.write_text(json.dumps(snapshot, indent=2))
    return out

def load_snapshot(date: str):
    p = SNAPSHOT_DIR / f"public-merged-{date}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())

def main():
    if len(sys.argv) < 2:
        print("Usage: snapshot.py <YYYY-MM-DD>")
        sys.exit(1)
    date = sys.argv[1]
    print(f"Listing public-merged/{date}/ ...")
    files = list_date_folder(date)
    out = save_snapshot(date, files)
    print(f"Saved {len(files)} files to {out}")

if __name__ == "__main__":
    main()