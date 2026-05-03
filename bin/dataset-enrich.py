#!/usr/bin/env python3
"""
Manifest-driven, CDN-bypass ingestion worker for surrogate-1.
Usage:
  python bin/dataset-enrich.py --shard 0 --date 2026-05-03
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from huggingface_hub import list_repo_tree

HF_REPO = "datasets/axentx/surrogate-1-training-pairs"
HF_TOKEN = os.getenv("HF_TOKEN")
OUT_ROOT = Path("batches/public-merged")
CDN_BASE = f"https://huggingface.co/datasets/{HF_REPO}/resolve/main"

# Schema-agnostic field projection
def project_to_pair(raw_bytes: bytes, ext: str) -> dict:
    """Return {prompt, response} or raise ValueError."""
    if ext == ".parquet":
        tbl = pq.read_table(pa.BufferReader(raw_bytes))
        # Try known schemas without enforcing full schema
        prompt_col = next((c for c in tbl.column_names if "prompt" in c.lower()), None)
        response_col = next((c for c in tbl.column_names if "response" in c.lower()), None)
        if prompt_col is None or response_col is None:
            raise ValueError("No prompt/response columns")
        # Take first row only for this worker (simplified)
        return {
            "prompt": str(tbl[prompt_col][0].as_py()),
            "response": str(tbl[response_col][0].as_py()),
        }
    elif ext == ".jsonl":
        lines = raw_bytes.decode().strip().splitlines()
        # Heuristic: first line with both fields
        for line in lines:
            obj = json.loads(line)
            if "prompt" in obj and "response" in obj:
                return {"prompt": str(obj["prompt"]), "response": str(obj["response"])}
    raise ValueError("Unrecognized schema")

def slug_hash_bucket(slug: str, n: int = 16) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % n

def build_manifest(date_folder: str) -> list:
    """Single API call: list top-level folder contents (non-recursive)."""
    items = list(list_repo_tree(HF_REPO, path=date_folder, recursive=False))
    files = [it for it in items if it.type == "file"]
    manifest = []
    for f in files:
        # Expect slug in filename or path; fallback to full path
        slug = f.path.split("/")[-1].split(".")[0]
        manifest.append({
            "path": f.path,
            "slug": slug,
            "cdn_url": f"{CDN_BASE}/{f.path}",
        })
    return manifest

def download_cdn(url: str) -> bytes:
    # No Authorization header -> bypasses /api/ rate limits
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.content

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=int, required=True, choices=range(16))
    parser.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    manifest = build_manifest(args.date)
    out_dir = OUT_ROOT / args.date
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%H%M%S")
    out_path = out_dir / f"shard{args.shard}-{ts}.jsonl"

    processed = 0
    skipped = 0
    for item in manifest:
        bucket = slug_hash_bucket(item["slug"])
        if bucket != args.shard:
            skipped += 1
            continue

        try:
            raw = download_cdn(item["cdn_url"])
            pair = project_to_pair(raw, Path(item["path"]).suffix)
            with out_path.open("a") as f:
                f.write(json.dumps(pair, ensure_ascii=False) + "\n")
            processed += 1
        except Exception as exc:
            # Log and continue to avoid losing entire shard
            print(f"WARN {item['path']}: {exc}", file=sys.stderr)

    print(f"Shard {args.shard}: processed={processed}, skipped={skipped}, out={out_path}")

if __name__ == "__main__":
    main()