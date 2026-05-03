#!/usr/bin/env python3
import json, os, sys, time
from huggingface_hub import HfApi

REPO = "datasets/axentx/surrogate-1-training-pairs"
FOLDER = sys.argv[1] if len(sys.argv) > 1 else "public-raw/2026-05-03"
OUT = sys.argv[2] if len(sys.argv) > 2 else f"manifest-{os.path.basename(FOLDER.rstrip('/'))}.json"
TOKEN = os.getenv("HF_TOKEN")

api = HfApi()
entries = api.list_repo_tree(
    repo_id=REPO,
    path=FOLDER,
    repo_type="dataset",
    recursive=False,
    token=TOKEN,
)

manifest = []
for e in entries:
    # Support both dict and str returns from hf_hub
    if isinstance(e, dict):
        if e.get("type") == "file":
            path = e["path"]
            size = e.get("size")
    else:
        path = str(e)
        size = None
    manifest.append({
        "path": path,
        "size": size,
        "cdn_url": f"https://huggingface.co/datasets/{REPO}/resolve/main/{path}"
    })

out_obj = {
    "repo_id": REPO,
    "folder": FOLDER,
    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "files": manifest,
}

with open(OUT, "w") as f:
    json.dump(out_obj, f, indent=2)

print(f"Wrote {len(manifest)} files to {OUT}")