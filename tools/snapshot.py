#!/usr/bin/env python3
"""
Generate deterministic file-list snapshot for a date folder in
datasets/axentx/surrogate-1-training-pairs.
Uses non-recursive tree listing to avoid pagination/rate-limit.
"""
import json
import os
import sys
from pathlib import Path

from huggingface_hub import HfApi

REPO = "datasets/axentx/surrogate-1-training-pairs"


def snapshot(date_folder: str, api: HfApi | None = None) -> list[dict]:
    api = api or HfApi()
    entries = api.list_repo_tree(repo_id=REPO, path=date_folder, recursive=False)
    files = []
    for e in entries:
        if e.type != "file":
            continue
        path = f"{date_folder}/{e.path}"
        files.append(
            {
                "path": path,
                "cdn_url": f"https://huggingface.co/{REPO}/resolve/main/{path}",
                "size": e.size or 0,
                "sha": getattr(e, "oid", None) or getattr(e, "sha", None) or "",
            }
        )
    files.sort(key=lambda x: x["path"])
    return files


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: snapshot.py <date_folder> <output.json>")
        sys.exit(1)
    date_folder, out_path = sys.argv[1], Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    files = snapshot(date_folder)
    out_path.write_text(
        json.dumps({"date_folder": date_folder, "files": files}, indent=2)
    )
    print(f"Wrote {len(files)} files to {out_path}")


if __name__ == "__main__":
    main()