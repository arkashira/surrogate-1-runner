#!/usr/bin/env python3
"""
Generate manifest.json for today's folder in axentx/surrogate-1-training-pairs.
Usage: python bin/generate_manifest.py
"""
import json
import os
import datetime
from pathlib import Path

from huggingface_hub import HfApi

HF_DATASET = "axentx/surrogate-1-training-pairs"

def main() -> None:
    api = HfApi()
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    tree = api.list_repo_tree(
        repo_id=HF_DATASET,
        repo_type="dataset",
        path=today,
    )
    files = [
        {"path": f.path, "sha": f.lfs.get("sha256", ""), "size": f.size}
        for f in tree
        if f.type == "file"
    ]

    manifest = {"date": today, "files": files}
    out_path = Path("manifest.json")
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote manifest with {len(files)} files to {out_path}")

if __name__ == "__main__":
    main()