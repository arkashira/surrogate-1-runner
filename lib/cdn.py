import time
import requests
from typing import Optional

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def cdn_download(repo: str, path: str, timeout: int = 30, retries: int = 3) -> bytes:
    """
    Download public dataset file via CDN (no Authorization header).
    CDN tier has much higher rate limits than /api/.
    """
    url = CDN_TEMPLATE.format(repo=repo, path=path)
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=timeout, headers={})
            resp.raise_for_status()
            return resp.content
        except requests.HTTPError as e:
            if resp.status_code == 429:
                wait = 360 if attempt == retries else (2 ** attempt) * 5
                print(f"CDN 429, waiting {wait}s (attempt {attempt}/{retries})")
                time.sleep(wait)
                continue
            raise
        except requests.RequestException:
            if attempt == retries:
                raise
            time.sleep((2 ** attempt) * 2)
    raise RuntimeError(f"Failed to download {url} after {retries} attempts")