#!/usr/bin/env python3
"""
Create a deterministic snapshot for a date folder in surrogate-1-training-pairs.
Usage:
  HF_TOKEN=<token> python bin/make-snapshot.py --date 2026-05-02 --out snapshot-2026-05-02.json
"""
import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi

API = HfApi()
REPO = "axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser(description="Create snapshot for a date folder.")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--repo", default=REPO, help="HF dataset repo")
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    # Non-recursive list per folder to avoid 100× pagination
    try:
        files = API.list_repo_tree(
            repo_id=args.repo,
            path=args.date,
            repo_type="dataset",
            token=token,
            recursive=False,
        )
    except Exception as e:
        print(f"ERROR listing repo tree: {e}", file=sys.stderr)
        sys.exit(1)

    snapshot = {
        "date": args.date,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "files": [
            {
                "file_path": f.rfilename if hasattr(f, "rfilename") else f["path"],
                "size": f.size if hasattr(f, "size") else f.get("size"),
                "sha": f.lfs.get("sha256") if hasattr(f, "lfs") else None,
            }
            for f in files
            if (hasattr(f, "type") and f.type == "file") or (isinstance(f, dict) and f.get("type") == "file")
        ],
    }

    with open(args.out, "w") as fp:
        json.dump(snapshot, fp, indent=2)

    print(f"Snapshot written to {args.out} ({len(snapshot['files'])} files)")

if __name__ == "__main__":
    main()