#!/usr/bin/env python3
"""
Generate snapshot of dataset files for a date folder.
Usage: python bin/lib/snapshot.py <repo> <date_folder> [output.json]
"""
import json
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

def generate_snapshot(repo: str, date_folder: str):
    api = HfApi()
    # list_repo_tree handles folder path; recursive=False lists immediate children
    tree = api.list_repo_tree(repo=repo, path=date_folder.rstrip("/"), recursive=False)
    files = [
        item.path
        for item in tree
        if item.type == "file" and item.path.lower().endswith((".parquet", ".jsonl"))
    ]
    snapshot = {
        "repo": repo,
        "date_folder": date_folder.rstrip("/"),
        "snapshot_ts": datetime.now(timezone.utc).isoformat(),
        "files": sorted(files),
        "count": len(files),
    }
    return snapshot

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: snapshot.py <repo> <date_folder> [output.json]")
        sys.exit(1)
    repo = sys.argv[1]
    date_folder = sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else "-"
    snapshot = generate_snapshot(repo, date_folder)
    if out_path == "-":
        json.dump(snapshot, sys.stdout, indent=2)
    else:
        with open(out_path, "w") as f:
            json.dump(snapshot, f, indent=2)