#!/usr/bin/env python3
"""
Run on Mac (or any machine with HF token) once per date folder.
Writes manifest.json with CDN-only URLs to avoid API rate limits during training.
Usage:
  HF_TOKEN=hf_xxx python tools/build_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --folder 2026-05-03 \
    --out manifest.json
"""
import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--folder", required=True, help="Subfolder in dataset repo (e.g. 2026-05-03)")
    parser.add_argument("--out", default="manifest.json")
    args = parser.parse_args()

    api = HfApi(token=os.getenv("HF_TOKEN"))
    entries = list(api.list_repo_tree(repo_id=args.repo, path=args.folder, recursive=False))

    files = [e for e in entries if e.type == "file"]
    if not files:
        print(f"No files found in {args.repo}/{args.folder}", file=sys.stderr)
        sys.exit(1)

    items = []
    for f in files:
        slug = os.path.splitext(os.path.basename(f.path))[0]
        items.append(
            {
                "slug": slug,
                "cdn_url": CDN_TEMPLATE.format(repo=args.repo, path=f.path),
                "source_path": f.path,
            }
        )

    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "repo": args.repo,
        "folder": args.folder,
        "items": items,
    }

    with open(args.out, "w", encoding="utf-8") as fp:
        json.dump(manifest, fp, indent=2)
    print(f"Wrote {len(items)} entries to {args.out}")

if __name__ == "__main__":
    main()