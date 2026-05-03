#!/usr/bin/env python3
"""
Generate manifest.json for surrogate-1 public dataset ingestion.
Run from Mac (or any dev machine) after HF API rate-limit window clears.
"""
import json, os, hashlib
from huggingface_hub import list_repo_tree

REPO = "axentx/surrogate-1-training-pairs"
OUT = "manifest.json"
N_SHARDS = 16

def shard_id(slug: str) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % N_SHARDS

def main():
    manifest = {"shards": {str(i): [] for i in range(N_SHARDS)}, "files": {}}
    # One folder per date: iterate top-level non-recursive
    for item in list_repo_tree(REPO, path="", recursive=False):
        if item.type != "directory":
            continue
        date = item.path
        for f in list_repo_tree(REPO, path=date, recursive=False):
            if f.type != "file":
                continue
            slug = f"{date}/{f.path}"
            sid = shard_id(slug)
            entry = {
                "slug": slug,
                "cdn_url": f"https://huggingface.co/datasets/{REPO}/resolve/main/{slug}",
                "shard": sid,
            }
            manifest["shards"][str(sid)].append(entry)
            manifest["files"][slug] = entry

    os.makedirs(os.path.dirname(OUT) if os.path.dirname(OUT) else ".", exist_ok=True)
    with open(OUT, "w") as fp:
        json.dump(manifest, fp, indent=2)
    print(f"Wrote {OUT} with {len(manifest['files'])} files across {N_SHARDS} shards.")

if __name__ == "__main__":
    main()