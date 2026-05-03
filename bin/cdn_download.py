#!/usr/bin/env python3
"""
Download dataset files via CDN (no auth/API) and project to {prompt, response}.

Usage:
  python3 bin/cdn_download.py <file-list.json> <out-dir> <repo>
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, Generator, List

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from tqdm import tqdm

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def cdn_lines(repo: str, path: str) -> Generator[Dict[str, Any], None, None]:
    url = CDN_TEMPLATE.format(repo=repo, path=path)
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            obj = json.loads(line)
            yield {
                "prompt": obj.get("prompt", ""),
                "response": obj.get("response", ""),
            }

def cdn_parquet(repo: str, path: str) -> Generator[Dict[str, Any], None, None]:
    url = CDN_TEMPLATE.format(repo=repo, path=path)
    # Stream into memory buffer then read parquet (avoids full copy on disk)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        buf = pa.BufferReader(r.content)
        table = pq.read_table(buf)
        for batch in table.to_batches():
            df = batch.to_pandas()
            for _, row in df.iterrows():
                yield {
                    "prompt": str(row.get("prompt", "")),
                    "response": str(row.get("response", "")),
                }

def download_all(file_list_path: str, out_dir: str, repo: str) -> List[str]:
    with open(file_list_path) as f:
        meta = json.load(f)

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    out_files: List[str] = []
    for item in tqdm(meta["files"], desc="CDN download"):
        src = item["path"]
        name = Path(src).name

        if src.endswith(".jsonl"):
            dst = out_path / name
            with open(dst, "w") as f:
                for row in cdn_lines(repo, src):
                    json.dump(row, f)
                    f.write("\n")
            out_files.append(str(dst))

        elif src.endswith(".parquet"):
            dst = out_path / name.replace(".parquet", ".jsonl")
            with open(dst, "w") as f:
                for row in cdn_parquet(repo, src):
                    json.dump(row, f)
                    f.write("\n")
            out_files.append(str(dst))

        else:
            # skip unknown extensions
            continue

    return out_files

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: cdn_download.py <file-list.json> <out-dir> <repo>")
        sys.exit(1)
    _, file_list, out_dir, repo = sys.argv
    download_all(file_list, out_dir, repo)