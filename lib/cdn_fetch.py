import json
import time
import requests
from pathlib import Path
from typing import Iterator, Tuple, Dict, Any, Optional

CDN_ROOT = "https://huggingface.co/datasets"

def cdn_url(repo: str, filepath: str) -> str:
    return f"{CDN_ROOT}/{repo}/resolve/main/{filepath}"

def stream_cdn_files(file_list_path: Path, repo: str) -> Iterator[Tuple[str, bytes]]:
    """Yield (filepath, raw_bytes) for each file in file-list.json via CDN."""
    listing = json.loads(file_list_path.read_text(encoding="utf-8"))
    files = listing.get("files", [])
    for fp in files:
        url = cdn_url(repo, fp)
        for attempt in range(5):
            try:
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                yield fp, resp.content
                break
            except Exception:
                if attempt == 4:
                    raise
                time.sleep((2 ** attempt) + (attempt * 0.1))

def project_to_pair(raw: bytes, filepath: str) -> Optional[Dict[str, Any]]:
    """
    Project raw file bytes into {prompt,response}.
    Implement per your schema rules. Examples:
    - JSON/JSONL: parse and map fields.
    - Text: treat as prompt, generate/derive response or skip.
    - Parquet/Arrow: decode and map columns.

    Return None to skip file.
    """
    # Placeholder: adapt to your actual schema.
    # Example for JSON lines:
    #   for line in raw.decode("utf-8").splitlines():
    #       obj = json.loads(line)
    #       return {"prompt": obj["input"], "response": obj["output"]}
    return None