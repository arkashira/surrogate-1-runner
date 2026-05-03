#!/usr/bin/env python3
"""
Generate manifest.json for a date folder to avoid recursive HF API calls.
Run once per cron (Mac/lightweight) and upload as artifact.
"""
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import list_repo_tree

REPO = "axentx/surrogate-1-training-pairs"
DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
OUT = "manifest.json"

def main() -> None:
    # Expect date override via env or arg
    date = sys.argv[1] if len(sys.argv) > 1 else DATE
    prefix = f"{date}/"

    entries = list_repo_tree(REPO, path=prefix, recursive=False)
    files = [e.r_path for e in entries if e.type == "file"]

    manifest = {
        "date": date,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": sorted(files),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote {len(files)} files to {OUT}")

if __name__ == "__main__":
    main()