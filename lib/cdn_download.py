import time
import requests
from pathlib import Path
from typing import Optional

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def cdn_download(
    repo: str,
    path: str,
    out_path: Path,
    max_retries: int = 5,
    backoff: float = 1.0,
) -> Path:
    """
    Download a dataset file via public CDN (no auth).
    Retries on transient failures.
    """
    url = CDN_TEMPLATE.format(repo=repo, path=path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, stream=True, timeout=30)
            resp.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return out_path
        except Exception as exc:
            if attempt == max_retries:
                raise
            sleep_sec = backoff * (2 ** (attempt - 1))
            print(f"Download failed ({exc}), retry {attempt}/{max_retries} in {sleep_sec}s: {url}")
            time.sleep(sleep_sec)
    raise RuntimeError("Unreachable")