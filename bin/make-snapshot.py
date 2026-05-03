#!/usr/bin/env python3
"""
Create a deterministic pre-flight snapshot for a date folder.
Usage:
    DATE=2024-06-01 python3 bin/make-snapshot.py
"""
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

REPO = os.environ.get("REPO", "axentx/surrogate-1-training-pairs")
DATE = os.environ.get("DATE", datetime.utcnow().strftime("%Y-%m-%d"))
OUT_DIR = os.environ.get("OUT_DIR", "snapshot")
OUT_FILE = os.path.join(OUT_DIR, DATE, "file-list.json")

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

api = HfApi()

try:
    tree = api.list_repo_tree(repo=REPO, path=DATE, recursive=False)
except Exception as e:
    # Fallback: list root and filter by date prefix
    try:
        tree = api.list_repo_tree(repo=REPO, path="", recursive=False)
        tree = [t for t in tree if t.path.startswith(f"{DATE}/")]
    except Exception as e2:
        print(f"Failed to list repo: {e2}", file=sys.stderr)
        sys.exit(1)

files = []
for t in tree:
    if getattr(t, "type", None) != "file":
        continue
    files.append({
        "path": t.path,
        "size": getattr(t, "size", None),
        "sha": getattr(t, "sha", None),
        "date": DATE,
    })

with open(OUT_FILE, "w") as f:
    json.dump(files, f, indent=2)

print(f"Wrote {len(files)} files to {OUT_FILE}")
sys.exit(0)