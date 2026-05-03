#!/usr/bin/env python3
"""
Generate a date-scoped manifest for axentx/surrogate-1-training-pairs.
Run on Mac (or cron) once per date after rate-limit window clears.

Outputs: manifests/YYYY-MM-DD.json  (list of {"path": str, "size": int})
"""
import json, os, sys, datetime
from huggingface_hub import HfApi

REPO = "datasets/axentx/surrogate-1-training-pairs"
OUT_DIR = "manifests"

def main():
    api = HfApi()
    date_str = datetime.date.today().isoformat()
    out_path = os.path.join(OUT_DIR, f"{date_str}.json")
    os.makedirs(OUT_DIR, exist_ok=True)

    # Single API call: non-recursive per top-level folder (avoid list_repo_files)
    items = api.list_repo_tree(repo_id=REPO, path="", recursive=True)
    files = [{"path": i.path, "size": i.size or 0} for i in items if i.type == "file"]

    with open(out_path, "w") as f:
        json.dump({"date": date_str, "repo": REPO, "files": files}, f, indent=2)

    print(f"Wrote {len(files)} files -> {out_path}")

if __name__ == "__main__":
    main()