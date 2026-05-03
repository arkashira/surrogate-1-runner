import json
import time
import requests
from typing import Iterator, Dict, Any

HEADERS = {"User-Agent": "axentx-surrogate-1/1.0"}

def cdn_stream(entries: list[Dict[str, str]]) -> Iterator[Dict[str, Any]]:
    """
    Stream JSONL lines from CDN URLs.
    Each entry: {"path": "...", "cdn_url": "..."}
    Yields {"prompt": ..., "response": ..., "_source": path}
    """
    for entry in entries:
        url = entry["cdn_url"]
        path = entry["path"]
        retries = 3
        for attempt in range(1, retries + 1):
            try:
                with requests.get(url, headers=HEADERS, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    for line in r.iter_lines(decode_unicode=True):
                        if not line or line.isspace():
                            continue
                        try:
                            obj = json.loads(line)
                            # Normalize to {prompt, response}
                            prompt = obj.get("prompt") or obj.get("input") or obj.get("question")
                            response = obj.get("response") or obj.get("output") or obj.get("answer")
                            if prompt is None or response is None:
                                continue
                            yield {"prompt": prompt, "response": response, "_source": path}
                        except json.JSONDecodeError:
                            continue
                break
            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    wait = 2 ** attempt * 5
                    print(f"CDN 429 on {url}, sleeping {wait}s")
                    time.sleep(wait)
                    continue
                raise
            except requests.RequestException as e:
                if attempt == retries:
                    print(f"Failed to stream {url}: {e}")
                    raise
                time.sleep(2 ** attempt)