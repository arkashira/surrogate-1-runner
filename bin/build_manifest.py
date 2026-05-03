#!/usr/bin/env python3
"""
One-time manifest builder for a date folder.
Usage:
  python3 bin/build_manifest.py --date 2026-05-03 --out manifests/2026-05-03/manifest.json
"""

import argparse
import json
from pathlib import Path

from huggingface_hub import HfApi

HF_REPO = "datasets/axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-03")
    parser.add_argument("--out", required=True, help="Output manifest path")
    args = parser.parse_args()

    api = HfApi()
    items = api.list_repo_tree(
        repo_id=HF_REPO,
        path=args.date,
        recursive=False,
        repo_type="dataset",
    )
    files = [it.rfilename for it in items if it.type == "file"]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(files, f, indent=2)

    print(f"Wrote {len(files)} entries -> {out_path}")

if __name__ == "__main__":
    main()