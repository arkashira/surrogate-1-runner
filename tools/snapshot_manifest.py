#!/usr/bin/env python3
"""
Generate CDN-only manifest for a date partition in axentx/surrogate-1-training-pairs.

Usage:
    python tools/snapshot_manifest.py --repo axentx/surrogate-1-training-pairs \
        --date 2026-04-29 --out manifests/2026-04-29_manifest.json
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List

from huggingface_hub import HfApi

HF_API = HfApi()

def build_manifest(repo: str, date_partition: str) -> List[Dict]:
    entries = HF_API.list_repo_tree(
        repo_id=repo,
        path=date_partition,
        recursive=True,
        repo_type="dataset",
    )

    manifest = []
    for entry in entries:
        if entry.type != "file":
            continue

        cdn_url = (
            f"https://huggingface.co/datasets/{repo}/resolve/main/{entry.path}"
        )
        item = {
            "repo": repo,
            "path": entry.path,
            "size": entry.size,
            "cdn_url": cdn_url,
        }

        # Include LFS metadata when available
        if getattr(entry, "lfs", None):
            item["lfs"] = {
                "oid": entry.lfs.get("oid"),
                "size": entry.lfs.get("size"),
            }
        manifest.append(item)

    # Deterministic ordering
    manifest.sort(key=lambda x: x["path"])
    return manifest

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CDN manifest for a date partition.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Date partition (e.g. 2026-04-29)")
    parser.add_argument("--out", help="Output JSON path")
    args = parser.parse_args()

    out_path = Path(args.out or f"manifests/{args.date}_manifest.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(args.repo, args.date)
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(manifest)} files to {out_path}")

if __name__ == "__main__":
    main()