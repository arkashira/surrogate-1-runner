#!/usr/bin/env python3
"""
Generate a deterministic file manifest for a single date partition.
Run on Mac (or any dev host) when rate-limit window is clear.

Usage:
  python bin/snapshot_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --out training/file_manifest.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi


def build_manifest(repo_id: str, date: str, out_path: str) -> None:
    api = HfApi()
    folder = f"batches/public-merged/{date}"

    try:
        entries = api.list_repo_tree(repo_id=repo_id, path=folder, recursive=False)
    except Exception as exc:
        print(f"HF API error listing {repo_id}/{folder}: {exc}", file=sys.stderr)
        sys.exit(1)

    files = sorted(e.rfilename for e in entries if e.rfilename.endswith(".parquet"))

    manifest = {
        "repo_id": repo_id,
        "date": date,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "cdn_base": f"https://huggingface.co/datasets/{repo_id}/resolve/main",
    }

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(files)} files to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create CDN file manifest.")
    parser.add_argument("--repo", required=True, help="HF dataset repo id")
    parser.add_argument("--date", required=True, help="Date partition (YYYY-MM-DD)")
    parser.add_argument("--out", default="training/file_manifest.json", help="Output JSON path")
    args = parser.parse_args()
    build_manifest(args.repo, args.date, args.out)