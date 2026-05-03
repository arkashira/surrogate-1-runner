#!/usr/bin/env python3
"""
Build per-folder manifest for surrogate-1 dataset using list_repo_tree.
Run from Mac/cron after HF API rate-limit window clears.
"""
import json, os, hashlib
from pathlib import Path
from huggingface_hub import HfApi

API = HfApi()
REPO = "datasets/axentx/surrogate-1-training-pairs"
OUT_DIR = Path(__file__).parent.parent / "manifests"

def build_manifest(date_folder: str):
    # date_folder like "public-merged/2026-04-30"
    entries = API.list_repo_tree(REPO, path=date_folder, recursive=False)
    files = []
    for e in entries:
        if e.type != "file":
            continue
        files.append({
            "path": f"{date_folder}/{e.path.split('/')[-1]}",
            "size": getattr(e, "size", None),
        })
    out_path = OUT_DIR / date_folder.replace("/", "_") / "files.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(files, indent=2))
    print(f"Wrote {len(files)} entries to {out_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: build-manifest.py <date-folder>")
        sys.exit(1)
    build_manifest(sys.argv[1])