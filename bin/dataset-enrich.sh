# Near top of bin/dataset-enrich.sh
MANIFEST_FILE="${MANIFEST_FILE:-}"

# Replace dataset file listing logic with:
if [[ -n "$MANIFEST_FILE" && -f "$MANIFEST_FILE" ]]; then
  echo "Using file list from manifest: $MANIFEST_FILE"
  mapfile -t HF_FILES < <(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for item in data.get('files', []):
    print(item['path'])
" "$MANIFEST_FILE")
else
  echo "Listing repo files via API (fallback)..."
  mapfile -t HF_FILES < <(python3 - <<PY
from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_files(repo_id="${HF_REPO}", repo_type="dataset")
for f in files:
    print(f)
PY
)
fi