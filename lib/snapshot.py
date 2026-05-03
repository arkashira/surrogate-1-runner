from __future__ import annotations
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

HF_REPO = os.getenv("HF_DATASET_REPO", "datasets/axentx/surrogate-1-training-pairs")

def run_hf_tree(path: str = "", recursive: bool = False) -> List[Dict[str, Any]]:
    """List repo tree via huggingface_hub (non-recursive by default)."""
    cmd = [
        "python3",
        "-c",
        (
            "from huggingface_hub import HfApi; "
            "import json, sys; "
            f"api = HfApi(); "
            f"tree = api.list_repo_tree(repo_id='{HF_REPO}', path='{path}', recursive={recursive}); "
            "print(json.dumps([t.to_dict() for t in tree]))"
        ),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def build_snapshot(date_folder: str) -> Dict[str, Any]:
    """
    Build manifest for a date folder (non-recursive).
    date_folder examples: '2026-04-29' or 'public-merged/2026-04-29'
    """
    tree = run_hf_tree(path=date_folder, recursive=False)
    files: List[Dict[str, Any]] = []
    for node in tree:
        if node.get("type") != "file":
            continue
        path = node["path"]
        cdn_url = f"https://huggingface.co/datasets/{HF_REPO}/resolve/main/{path}"
        files.append(
            {
                "path": path,
                "cdn_url": cdn_url,
                "size": node.get("size"),
                "lfs": node.get("lfs", {}),
            }
        )

    snapshot = {
        "repo": HF_REPO,
        "date_folder": date_folder,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": sorted(files, key=lambda x: x["path"]),
        "count": len(files),
    }
    return snapshot

def save_snapshot(snapshot: Dict[str, Any], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d%H%M")
    fname = out_dir / f"snapshot-{ts}.json"
    fname.write_text(json.dumps(snapshot, indent=2))
    return fname

def load_snapshot(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: snapshot.py <date-folder> [out-dir]", file=sys.stderr)
        sys.exit(1)
    date_folder = sys.argv[1]
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("batches/public-merged")
    snap = build_snapshot(date_folder)
    p = save_snapshot(snap, out_dir)
    print(str(p))