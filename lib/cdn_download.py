import time
import urllib.request
import urllib.error
import hashlib
import os
from typing import Optional

def stable_hash_int(s: str) -> int:
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)

def cdn_fetch(url: str, out_path: str, max_retries: int = 5, timeout: int = 30) -> bool:
    attempt = 0
    while attempt < max_retries:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "training-ingest/1.0 (+https://huggingface.co/datasets)"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                with open(out_path, "wb") as f:
                    f.write(resp.read())
            return True
        except urllib.error.HTTPError as e:
            # Do not retry 4xx except 429; 404 is permanent
            if e.code in (400, 401, 403, 404, 422):
                return False
        except (urllib.error.URLError, TimeoutError, OSError):
            pass

        attempt += 1
        sleep_sec = min(2 ** attempt, 60)
        time.sleep(sleep_sec)
    return False