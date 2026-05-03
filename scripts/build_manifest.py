#!/usr/bin/env python3
"""
Run on Mac after HF rate-limit window clears.
Generates train/manifest.json so training uses CDN-only fetches.
"""
import json
from pathlib import Path
from huggingface_hub import HfApi

API = HfApi()
REPO = "axentx/surrogate-1-training-pairs"
OUT = Path(__file__).parent.parent / "train" / "manifest.json"

def main():
    OUT.parent.mkdir(exist_ok=True)
    tree = API.list_repo_tree(REPO, path="batches/public-merged", recursive=False)
    manifest = {"repos": [], "shards": {}}

    for entry in tree:
        # entry.path like "batches/public-merged/2026-05-03/"
        if entry.type != "directory":
            continue
        date = Path(entry.path).name
        day_tree = API.list_repo_tree(REPO, path=entry.path, recursive=False)
        files = [
            f"{date}/{Path(e.path).name}"
            for e in day_tree
            if e.type == "file" and e.path.endswith(".parquet")
        ]
        if files:
            manifest["shards"][date] = files

    # sibling repo assignment (5 siblings)
    manifest["repos"] = [
        f"axentx/surrogate-1-training-pairs-{i}" for i in range(5)
    ]

    OUT.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {OUT} with {sum(len(v) for v in manifest['shards'].values())} files")

if __name__ == "__main__":
    main()