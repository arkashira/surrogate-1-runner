import requests
import time
from typing import BinaryIO

def stream_cdn_file(repo: str, path: str, chunk_size: int = 8192, retries: int = 3, timeout: int = 30) -> BinaryIO:
    """
    Stream file via CDN (no Authorization header).
    Returns raw file-like object. Raises on final failure.
    """
    url = f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, stream=True, timeout=timeout)
            resp.raise_for_status()
            return resp.raw
        except Exception as exc:
            if attempt == retries:
                raise RuntimeError(f"CDN fetch failed for {repo}/{path} after {retries} attempts") from exc
            wait = 2 ** attempt
            print(f"CDN fetch failed ({exc}) for {path}, retry {attempt}/{retries} in {wait}s")
            time.sleep(wait)