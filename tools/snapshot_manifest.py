#!/usr/bin/env python3
"""
Generate a CDN-only file manifest for one date-partition in a HuggingFace dataset repo.

Usage:
    python tools/snapshot_manifest.py \
        --repo axentx/surrogate-1-training-pairs \
        --date 2026-04-29 \
        --out file_manifest.json
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import list_repo_tree
from tqdm import tqdm

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def build_manifest(repo: str, date_partition: str, out_path: str) -> None:
    # Single API call: list one folder (date partition)
    entries = list(
        list_repo_tree(
            repo_id=repo,
            path=date_partition,
            recursive=True,
            repo_type="dataset",
        )
    )
    files = [e for e in entries if e.type == "file"]
    if not files:
        print(f"No files found under {repo}/{date_partition}", file=sys.stderr)
        sys.exit(1)

    manifest_files = []
    for f in tqdm(files, desc="Building manifest"):
        manifest_files.append(
            {
                "repo": repo,
                "path": f.path,
                "cdn_url": CDN_TEMPLATE.format(repo=repo, path=f.path),
                "size": getattr(f, "size", None),
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": repo,
        "date_partition": date_partition,
        "files": manifest_files,
    }

    # Deterministic sha256 for reproducibility
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["manifest_sha256"] = hashlib.sha256(canonical).hexdigest()

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2, sort_keys=True)

    print(f"Wrote {len(manifest_files)} files -> {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate CDN file manifest.")
    parser.add_argument("--repo", required=True, help="HF dataset repo (e.g. axentx/surrogate-1-training-pairs)")
    parser.add_argument("--date", required=True, help="Date partition folder (e.g. 2026-04-29)")
    parser.add_argument("--out", default="file_manifest.json", help="Output JSON path")
    args = parser.parse_args()
    build_manifest(args.repo, args.date, args.out)