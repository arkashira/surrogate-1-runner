import json
import time
import hashlib
from pathlib import Path
from typing import Iterator, Dict, Any, Optional

import requests
from requests.adapters import HTTPAdapter, Retry

CDN_ROOT = "https://huggingface.co/datasets"

def cdn_url(repo: str, path: str) -> str:
    return f"{CDN_ROOT}/{repo}/resolve/main/{path}"

def _make_session() -> requests.Session:
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist={429, 500, 502, 503, 504},
        allowed_methods={"GET", "HEAD"},
    )
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s

_SESSION = _make_session()

def stream_jsonl_cdn(
    repo: str,
    filepath: str,
    expected_size: Optional[int] = None,
    chunk_size: int = 8192,
) -> Iterator[Dict[str, Any]]:
    url = cdn_url(repo, filepath)
    with _SESSION.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        if expected_size is not None:
            got = int(r.headers.get("content-length", 0))
            if got != expected_size:
                raise ValueError(f"Size mismatch for {filepath}: expected {expected_size}, got {got}")

        buffer = ""
        for chunk in r.iter_content(chunk_size=chunk_size, decode_unicode=True):
            if not chunk:
                continue
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if line:
                    yield json.loads(line)

def load_manifest(manifest_path: str) -> Dict[str, Any]:
    with open(manifest_path, encoding="utf-8") as f:
        return json.load(f)