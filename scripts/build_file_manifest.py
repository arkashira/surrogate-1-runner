import os, json, datetime
from huggingface_hub import HfApi

REPO = "axentx/surrogate-1-training-pairs"
OUT_DIR = "manifests"
os.makedirs(OUT_DIR, exist_ok=True)

api = HfApi()
date_folder = datetime.date.today().isoformat()  # or pass as arg

# One non-recursive API call per folder
tree = api.list_repo_tree(REPO, path=date_folder, recursive=False)
files = [item.rfilename for item in tree if item.type == "file"]

manifest = {
    "repo": REPO,
    "folder": date_folder,
    "files": sorted(files),
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z"
}

out_path = os.path.join(OUT_DIR, f"file-list-{date_folder}.json")
with open(out_path, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Wrote {len(files)} files to {out_path}")