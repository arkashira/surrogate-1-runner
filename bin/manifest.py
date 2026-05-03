#!/usr/bin/env python3
"""
Generate manifest for a date folder.
Usage:
  python bin/manifest.py --repo axentx/surrogate-1-training-pairs \
                         --date 2026-05-03 \
                         --out manifest-2026-05-03.json
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    from huggingface_hub import list_repo_tree
except ImportError:
    print("pip install huggingface_hub")
    sys.exit(1)

HF_TOKEN = os.getenv("HF_TOKEN")

def build_manifest(repo: str, date: str, out_path: str):
    # date folder at repo root, e.g. raw/2026-05-03/
    path = f"raw/{date}"
    print(f"Listing {repo}/{path} ...")
    tree = list_repo_tree(
        repo_id=repo,
        path=path,
        recursive=True,
        token=HF_TOKEN,
    )
    files = [item.path for item in tree if item.type == "file"]
    manifest = {
        "repo": repo,
        "date": date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": sorted(files),
    }
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {len(files)} files -> {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--out", default="manifest.json")
    args = p.parse_args()
    build_manifest(args.repo, args.date, args.out)