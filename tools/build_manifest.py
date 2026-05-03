import json
import os
import sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

HF_REPO = "datasets/axentx/surrogate-1-training-pairs"
OUT_DIR = "manifests"
os.makedirs(OUT_DIR, exist_ok=True)

api = HfApi()

def build_manifest_for_date(date_folder: str):
    """
    date_folder example: "2026-04-29"
    Uses non-recursive list_repo_tree to avoid pagination/rate limits.
    """
    entries = api.list_repo_tree(
        repo_id=HF_REPO,
        path=date_folder,
        repo_type="dataset",
        recursive=False,
    )

    files = []
    for e in entries:
        if not e.path.endswith((".parquet", ".jsonl", ".csv")):
            continue
        cdn_url = f"https://huggingface.co/datasets/{HF_REPO}/resolve/main/{e.path}"
        files.append({
            "path": e.path,
            "cdn_url": cdn_url,
            "size": getattr(e, "size", None),
        })

    manifest = {
        "date_folder": date_folder,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repo": HF_REPO,
        "files": files,
        "total_files": len(files),
    }

    out_path = os.path.join(OUT_DIR, f"manifest-{date_folder}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote {out_path} ({len(files)} files)")
    return out_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_manifest.py <date_folder>")
        sys.exit(1)
    build_manifest_for_date(sys.argv[1])