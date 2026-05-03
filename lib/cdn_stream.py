import io
import time
import requests
from typing import BinaryIO, Optional

def cdn_stream(cdn_url: str, max_retries: int = 5, timeout: int = 30) -> BinaryIO:
    """
    Stream a dataset file from HF CDN with exponential backoff.
    Uses no Authorization header — CDN tier has separate (higher) rate limits.
    """
    headers = {}
    for attempt in range(max_retries):
        try:
            resp = requests.get(cdn_url, headers=headers, timeout=timeout, stream=True)
            resp.raise_for_status()
            # Wrap raw bytes into file-like object
            raw = io.BytesIO()
            for chunk in resp.iter_content(chunk_size=8192):
                raw.write(chunk)
            raw.seek(0)
            return raw
        except requests.HTTPError as e:
            if resp.status_code == 429:
                wait = 360 if attempt == 0 else (2 ** attempt) * 5
                time.sleep(wait)
                continue
            raise
        except (requests.RequestException, OSError) as e:
            if attempt == max_retries - 1:
                raise
            time.sleep((2 ** attempt) * 2)
    raise RuntimeError("Exhausted retries")