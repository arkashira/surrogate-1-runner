import requests
from pathlib import Path
from huggingface_hub import hf_hub_download
import time

def cdn_fetch(path: str, repo: str, out_path: Path, max_retries: int = 3):
    url = f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            out_path.write_bytes(resp.content)
            return out_path
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    return out_path

def fetch_file(path: str, repo: str, out_path: Path, use_cdn: bool = True):
    if use_cdn:
        try:
            return cdn_fetch(path, repo, out_path)
        except Exception:
            pass
    return Path(hf_hub_download(repo_id=repo, filename=path, cache_dir=out_path.parent))