#!/usr/bin/env python3
"""
Generate manifest/<DATE_FOLDER>.json listing all files under that folder
(non-recursive tree walk) to avoid HF API list_repo_files recursion/429.
Run from Mac orchestrator after rate-limit window or on first miss.
"""
import os
import json
from datetime import datetime, timezone
from huggingface_hub import HfApi

REPO = "datasets/axentx/surrogate-1-training-pairs"
OUT_DIR = "manifest"

def main(date_folder: str | None = None):
    if date_folder is None:
        date_folder = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(OUT_DIR, exist_ok=True)
    api = HfApi()
    # Single call per folder; avoid recursive=True on big repos
    tree = api.list_repo_tree(repo_id=REPO, path=date_folder, recursive=False)
    files = [item.rfilename for item in tree if item.type == "file"]
    # If folders exist, we could recurse one level only as needed.
    manifest_path = os.path.join(OUT_DIR, f"{date_folder}.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"date_folder": date_folder, "files": sorted(files)}, f, indent=2)
    print(f"Wrote {len(files)} files to {manifest_path}")

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)