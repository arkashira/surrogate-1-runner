#!/usr/bin/env python3
import argparse, json, os, hashlib
from pathlib import Path
from huggingface_hub import hf_hub_download, upload_file
from datasets import load_dataset
import pyarrow as pa
import numpy as np

HF_REPO = "axentx/surrogate-1-training-pairs"

def shard_for(slug: str, n_shards: int = 16) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % n_shards

def safe_project_to_pair(file_path: str):
    """Download one file and project to {prompt, response} without schema assumptions."""
    local_path = hf_hub_download(repo_id=HF_REPO, filename=file_path, repo_type="dataset")
    try:
        ds = load_dataset("parquet", data_files=local_path, split="train")
    except (pa.ArrowInvalid, pa.ArrowTypeError):
        # fallback: try jsonl
        ds = load_dataset("json", data_files=local_path, split="train")

    pairs = []
    for row in ds:
        prompt = row.get("prompt") or row.get("input") or row.get("question") or ""
        response = row.get("response") or row.get("output") or row.get("answer") or ""
        if prompt and response:
            pairs.append({"prompt": str(prompt), "response": str(response)})
    return pairs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=int, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--manifest", default=None)
    args = parser.parse_args()

    manifest_path = args.manifest or f"manifests/{args.date}/file_list.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    my_files = [f for f in manifest["files"] if shard_for(f) == args.shard]
    print(f"Shard {args.shard}: processing {len(my_files)} files")

    from lib.dedup import DedupStore
    dedup = DedupStore()

    out_rows = []
    for rel_path in my_files:
        try:
            pairs = safe_project_to_pair(rel_path)
            for p in pairs:
                h = hashlib.md5(f"{p['prompt']}\n{p['response']}".encode()).hexdigest()
                if not dedup.seen(h):
                    dedup.add(h)
                    out_rows.append(p)
        except Exception as e:
            print(f"Error processing {rel_path}: {e}")

    if not out_rows:
        print("No new rows; skipping upload.")
        return

    ts = pd.Timestamp.utcnow().strftime("%H%M%S")
    out_name = f"shard{args.shard}-{ts}.jsonl"
    out_dir = f"batches/public-merged/{args.date}"
    out_path = Path(out_dir) / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w") as f:
        for row in out_rows:
            f.write(json.dumps(row) + "\n")

    upload_file(
        path_or_fileobj=out_path,
        path_in_repo=f"{out_dir}/{out_name}",
        repo_id=HF_REPO,
        repo_type="dataset",
    )
    print(f"Uploaded {len(out_rows)} rows -> {out_dir}/{out_name}")

if __name__ == "__main__":
    import pandas as pd
    main()