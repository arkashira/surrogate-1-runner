#!/usr/bin/env python3
import json
from datetime import date
from huggingface_hub import list_repo_tree

REPO_ID = "axentx/surrogate-1-training-pairs"
TODAY = str(date.today())
FOLDER = f"public-merged/{TODAY}"

entries = list_repo_tree(REPO_ID, path=FOLDER, recursive=False)
files = [e["path"] for e in entries if e["type"] == "file"]
files.sort()

manifest = {
    "repo_id": REPO_ID,
    "date": TODAY,
    "root": FOLDER,
    "files": files
}

out_path = f"manifests/{TODAY}.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(files)} files to {out_path}")