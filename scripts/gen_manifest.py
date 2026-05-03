#!/usr/bin/env python3
"""
Generate train_manifest.json for a date folder.
Usage: python gen_manifest.py axentx/surrogate-1-training-pairs 2026-05-03
"""
import json, sys, time
from pathlib import Path
from huggingface_hub import HfApi

API = HfApi()
REPO = sys.argv[1]
DATE = sys.argv[2]
FOLDER = f"batches/public-merged/{DATE}"
OUT = Path("manifests") / f"{DATE}.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

def backoff(attempt):
    t = 360 if attempt == 1 else 60 * attempt
    print(f"Rate limited — sleeping {t}s", file=sys.stderr)
    time.sleep(t)

for attempt in range(1, 4):
    try:
        tree = API.list_repo_tree(REPO, path=FOLDER, recursive=False)
        files = [item.path for item in tree if item.type == "file"]
        manifest = {"date": DATE, "folder": FOLDER, "files": sorted(files)}
        OUT.write_text(json.dumps(manifest, indent=2))
        print(f"Wrote {len(files)} files to {OUT}")
        break
    except Exception as e:
        if "429" in str(e):
            backoff(attempt)
        else:
            raise