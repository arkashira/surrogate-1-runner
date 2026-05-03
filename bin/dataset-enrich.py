#!/usr/bin/env python3
"""
Manifest-driven, CDN-bypass ingestion worker.

Environment:
  SHARD_ID     (int)   : shard index
  SHARD_TOTAL  (int)   : total shards
  DATE         (str)   : YYYY-MM-DD
  HF_TOKEN     (str)   : Hugging Face token with dataset read access
"""

import os
import sys
import json
import uuid
import shutil
import requests
from typing import List, Dict, Any

# ── Configuration ──────────────────────────────────────────────────────
REPO_ID = "axentx/surrogate-1-training-pairs"
BASE_URL = f"https://huggingface.co/datasets/{REPO_ID}"
HEADERS = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN', '')}"}
OUTPUT_DIR = os.path.join("batches", "public-merged", os.environ.get("DATE", ""))

# ── Helpers ────────────────────────────────────────────────────────────
def _get_manifest(date: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/resolve/main/{date}/manifest.json"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()

def _stream_download(url: str, dst: str) -> None:
    with requests.get(url, headers=HEADERS, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(dst, "wb") as f:
            shutil.copyfileobj(r.raw, f)

def _process_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Placeholder: implement domain-specific parsing/transformation.
    For JSONL inputs, this typically yields one record per line.
    """
    # Example for JSONL:
    # with open(filepath) as f:
    #     for line in f:
    #         yield json.loads(line)
    return []

def _write_output(records: List[Dict[str, Any]], date: str, shard_id: int) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    suffix = str(uuid.uuid4().int)[:6]  # short random suffix
    out_path = os.path.join(OUTPUT_DIR, f"shard{shard_id}-{suffix}.jsonl")
    with open(out_path, "w") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return out_path

# ── Main ───────────────────────────────────────────────────────────────
def main() -> None:
    try:
        shard_id = int(os.environ["SHARD_ID"])
        shard_total = int(os.environ["SHARD_TOTAL"])
        date = os.environ["DATE"]
    except KeyError as e:
        sys.stderr.write(f"Missing environment variable: {e}\n")
        sys.exit(1)
    except ValueError:
        sys.stderr.write("SHARD_ID and SHARD_TOTAL must be integers\n")
        sys.exit(1)

    if not os.environ.get("HF_TOKEN"):
        sys.stderr.write("HF_TOKEN is required\n")
        sys.exit(1)

    manifest = _get_manifest(date)
    files = manifest.get("files", [])
    if not files:
        sys.stderr.write(f"No files found in manifest for {date}\n")
        sys.exit(0)

    shard_files = [f for i, f in enumerate(files) if i % shard_total == shard_id]
    if not shard_files:
        sys.stderr.write(f"Shard {shard_id} has no files to process\n")
        sys.exit(0)

    all_records: List[Dict[str, Any]] = []
    for name in shard_files:
        remote_url = f"{BASE_URL}/resolve/main/{date}/{name}"
        tmp_path = os.path.join("/tmp", os.path.basename(name))
        try:
            _stream_download(remote_url, tmp_path)
            all_records.extend(_process_file(tmp_path))
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    if all_records:
        out_path = _write_output(all_records, date, shard_id)
        sys.stdout.write(f"Shard {shard_id} wrote {len(all_records)} records to {out_path}\n")
    else:
        sys.stdout.write(f"Shard {shard_id} produced no records\n")

if __name__ == "__main__":
    main()