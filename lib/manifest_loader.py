import json
import pyarrow.parquet as pq
import requests
from pathlib import Path
from typing import Iterator, Dict, Any

CDN_ROOT = "https://huggingface.co/datasets"

def load_manifest(manifest_path: str) -> Dict[str, Any]:
    with open(manifest_path) as f:
        return json.load(f)

def cdn_url(repo: str, file_path: str) -> str:
    return f"{CDN_ROOT}/{repo}/resolve/main/{file_path}"

def stream_from_manifest(
    manifest_path: str,
    columns=("prompt", "response"),
    tmp_dir: str = "/tmp"
) -> Iterator[Dict[str, Any]]:
    manifest = load_manifest(manifest_path)
    repo = manifest["repo"]
    tmp_path = Path(tmp_dir)
    tmp_path.mkdir(parents=True, exist_ok=True)

    for file_path in manifest["files"]:
        url = cdn_url(repo, file_path)
        local_path = tmp_path / Path(file_path).name
        if not local_path.exists():
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        try:
            table = pq.read_table(local_path, columns=columns)
            for batch in table.to_batches(max_chunksize=1024):
                for row in zip(*[batch.column(col).to_pylist() for col in columns]):
                    yield dict(zip(columns, row))
        finally:
            if local_path.exists():
                local_path.unlink()