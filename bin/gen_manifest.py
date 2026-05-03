#!/usr/bin/env python3
import json, os, hashlib
from huggingface_hub import HfApi

API = HfApi()
REPO = "axentx/surrogate-1-training-pairs"
DATE = os.getenv("DATE", "2026-05-03")  # e.g. 2026-05-03
OUT_DIR = f"manifests/{DATE}"
os.makedirs(OUT_DIR, exist_ok=True)

# Single API call: non-recursive per folder
tree = API.list_repo_tree(repo_id=REPO, path=f"batches/public-raw/{DATE}", recursive=False)
files = [f.rfilename for f in tree if f.rfilename.endswith(('.jsonl', '.parquet'))]

manifest = {
    "date": DATE,
    "files": files,
    "total": len(files),
    "checksum": hashlib.sha256(json.dumps(files).encode()).hexdigest()[:12]
}

out_path = f"{OUT_DIR}/file_list.json"
with open(out_path, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest written: {out_path} ({len(files)} files)")