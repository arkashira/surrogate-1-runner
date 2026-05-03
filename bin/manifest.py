#!/usr/bin/env python3
"""
Generate manifest for surrogate-1-training-pairs.
Run from Mac when HF API rate-limit window is clear.
Writes manifest.json with CDN-ready paths.
"""
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

REPO_ID = "axentx/surrogate-1-training-pairs"
OUTFILE = "manifest.json"

def main() -> None:
    api = HfApi()
    # Single non-recursive call per top-level folder (avoids 100x pagination)
    folders = ["batches/public-raw", "batches/mirror-merged"]
    entries = []
    for folder in folders:
        try:
            items = api.list_repo_tree(
                repo_id=REPO_ID,
                path=folder,
                recursive=False,
                repo_type="dataset",
            )
        except Exception as exc:
            print(f"Warning: failed to list {folder}: {exc}", file=sys.stderr)
            continue
        for item in items:
            if getattr(item, "type", None) != "file":
                continue
            path = getattr(item, "path", None)
            if not path:
                continue
            entries.append(
                {
                    "path": path,
                    "cdn_url": f"https://huggingface.co/datasets/{REPO_ID}/resolve/main/{path}",
                    "size": getattr(item, "size", None),
                }
            )

    manifest = {
        "repo_id": REPO_ID,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
        "count": len(entries),
    }
    with open(OUTFILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {OUTFILE} with {len(entries)} entries")

if __name__ == "__main__":
    main()