import argparse
import json
import os
import sys
from typing import List, Dict
from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def build_manifest(repo: str, date_partition: str, out_path: str) -> None:
    # ... (rest of the code remains the same)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create CDN manifest for HF dataset partition")
    parser.add_argument("--repo", required=True, help="HF dataset repo (e.g., user/repo)")
    parser.add_argument("--partition", required=True, help="Date partition path (e.g., 2026-04-29)")
    parser.add_argument("--out", default="file_manifest.json", help="Output JSON path")
    args = parser.parse_args()
    try:
        build_manifest(args.repo, args.partition, args.out)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)