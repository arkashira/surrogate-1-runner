import argparse
import json
from huggingface_hub import HfApi

def list_date_partition(date_folder, token):
    api = HfApi(token=token)
    entries = api.list_repo_tree(repo_id="axentx/surrogate-1-training-pairs", path=date_folder, recursive=False)
    files = []
    for entry in entries:
        if entry.type != "file":
            continue
        path = entry.path
        files.append({
            "path": path,
            "cdn_url": f"https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{path}",
            "size": getattr(entry, "size", None),
        })
    files.sort(key=lambda f: f["path"])
    return files

def main():
    parser = argparse.ArgumentParser(description="Create CDN manifest for a date partition.")
    parser.add_argument("--date", required=True, help="Date folder, e.g., batches/public-merged/2026-05-03")
    parser.add_argument("--out", default="file_manifest.json", help="Output JSON path")
    args = parser.parse_args()
    token = "YOUR_HF_TOKEN"
    files = list_date_partition(args.date, token)
    manifest = {
        "date_folder": args.date,
        "files": files,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    main()