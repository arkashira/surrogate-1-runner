import json
import os
import time
from pathlib import Path
from typing import List, Dict, Any
from huggingface_hub import HfApi, RepositoryError

api = HfApi()

def list_files_via_tree(repo: str, path: str = "", recursive: bool = False, 
                       max_retries: int = 3, backoff: int = 360) -> List[str]:
    """List files via repo tree with 429 backoff."""
    for attempt in range(max_retries):
        try:
            tree = api.list_repo_tree(
                repo=repo, path=path, repo_type="dataset", recursive=recursive
            )
            return [item.rfilename for item in tree if not item.rfilename.endswith("/")]
        except RepositoryError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Rate limited (429), sleeping {backoff}s...")
            time.sleep(backoff)
    return []

def save_snapshot(files: List[str], repo: str, date: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "repo": repo,
        "date": date,
        "files": sorted(files)
    }
    latest = out_dir / "snapshot-latest.json"
    with open(latest, "w") as f:
        json.dump(snapshot, f, indent=2)
    return latest

def load_snapshot(path: Path) -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)