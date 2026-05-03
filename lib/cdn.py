import json
import time
import requests
from pathlib import Path
from typing import List, Dict
from huggingface_hub import list_repo_tree

HF_DATASETS_BASE = "https://huggingface.co/datasets"

def build_cdn_url(repo: str, filepath: str) -> str:
    return f"{HF_DATASETS_BASE}/{repo}/resolve/main/{filepath}"

def robust_list_repo_tree(repo: str, folder: str = "", recursive: bool = True, max_retries: int = 3) -> List[Dict]:
    """One-time listing with 429 retry (Candidate 1 robustness)."""
    for attempt in range(1, max_retries + 1):
        try:
            return list(list_repo_tree(repo, folder=folder, recursive=recursive))
        except Exception as e:
            if hasattr(e, "response") and getattr(e.response, "status_code", None) == 429 and attempt < max_retries:
                wait = 60 * attempt
                time.sleep(wait)
                continue
            raise

def generate_file_list(repo: str, output_path: str, folder: str = "", recursive: bool = True) -> List[Dict]:
    items = robust_list_repo_tree(repo, folder=folder, recursive=recursive)
    files = [
        {"path": item.path, "cdn_url": build_cdn_url(repo, item.path), "size": getattr(item, "size", None)}
        for item in items
        if item.type == "file" and item.path.endswith((".jsonl", ".parquet", ".json"))
    ]
    Path(output_path).write_text(json.dumps(files, indent=2))
    print(f"Saved {len(files)} files to {output_path}")
    return files

def load_file_list(path: str) -> List[Dict]:
    return json.loads(Path(path).read_text())