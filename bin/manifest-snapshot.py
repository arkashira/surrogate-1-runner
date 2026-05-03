#!/usr/bin/env python3
"""
Generate file-list.json for surrogate-1-training-pairs.
Run from Mac (or any machine with HF token) when API rate-limit allows.
"""
import json
import os
from huggingface_hub import HfApi

REPO = "axentx/surrogate-1-training-pairs"
OUT = "file-list.json"

def main() -> None:
    api = HfApi(token=os.environ["HF_TOKEN"])
    # Only top-level listing to avoid 100x pagination; recurse by date folders if needed.
    files = api.list_repo_tree(repo_id=REPO, recursive=True)
    paths = [f.rfilename for f in files if f.rfilename.endswith((".parquet", ".jsonl", ".csv"))]
    with open(OUT, "w") as f:
        json.dump({"repo": REPO, "generated_by": "manifest-snapshot", "paths": paths}, f, indent=2)
    print(f"Wrote {len(paths)} paths to {OUT}")

if __name__ == "__main__":
    main()