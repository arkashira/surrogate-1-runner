#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in
axentx/surrogate-1-training-pairs to enable CDN-only ingestion.

Usage:
  python bin/list-date-files.py --date 2026-04-29 --out file-list-2026-04-29.json
"""
import argparse
import json
import sys
import time
from pathlib import Path

from huggingface_hub import HfApi, RateLimitError, RepositoryNotFoundError

REPO_ID = "datasets/axentx/surrogate-1-training-pairs"

def list_date_files(date_folder: str, out_path: Path, max_retries: int = 3) -> None:
    api = HfApi()
    for attempt in range(1, max_retries + 1):
        try:
            entries = api.list_repo_tree(
                repo_id=REPO_ID,
                path=date_folder,
                repo_type="dataset",
                recursive=False,
            )
            files = [e.rfilename for e in entries if e.type == "file"]
            out_path.write_text(json.dumps({"date": date_folder, "files": files}, indent=2))
            print(f"Wrote {len(files)} files to {out_path}")
            return
        except RateLimitError:
            wait = 360
            print(f"Rate limited (429). Waiting {wait}s (attempt {attempt}/{max_retries})", file=sys.stderr)
            time.sleep(wait)
        except RepositoryNotFoundError:
            print(f"Repo not found: {REPO_ID}", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"Unexpected error: {exc}", file=sys.stderr)
            if attempt == max_retries:
                sys.exit(1)
            time.sleep(5 * attempt)

    print("Max retries exceeded.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List date folder files for CDN ingestion.")
    parser.add_argument("--date", required=True, help="Date folder (e.g., 2026-04-29)")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()
    list_date_files(args.date, Path(args.out))