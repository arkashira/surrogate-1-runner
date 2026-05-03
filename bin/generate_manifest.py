#!/usr/bin/env python3
"""
Generate manifest for a date folder.
Usage:
  HF_TOKEN=... python bin/generate_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --out manifest-2026-05-03.json
"""
import argparse
import json
import os
from datetime import datetime

from huggingface_hub import HfApi

HF_API = HfApi(token=os.getenv("HF_TOKEN"))

def build_manifest(repo_id: str, date: str, out_path: str, n_shards: int = 16):
    folder = f"batches/public-merged/{date}"
    items = HF_API.list_repo_tree(repo_id=repo_id, path=folder, recursive=False)
    files = [it for it in items if it.path.endswith(".parquet")]

    manifest = {
        "repo_id": repo_id,
        "date": date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "n_shards": n_shards,
        "files": [],
    }

    for f in files:
        import hashlib
        shard_id = int(hashlib.md5(f.path.encode()).hexdigest(), 16) % n_shards
        manifest["files"].append({
            "path": f.path,
            "cdn_url": f"https://huggingface.co/datasets/{repo_id}/resolve/main/{f.path}",
            "schema_tag": "public",  # could be inferred from path if needed
            "shard_id": shard_id,
        })

    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {len(files)} files to {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--date", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--n-shards", type=int, default=16)
    args = p.parse_args()
    build_manifest(args.repo, args.date, args.out, args.n_shards)