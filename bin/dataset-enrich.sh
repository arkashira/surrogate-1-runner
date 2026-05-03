# Near top, after defaults
SNAPSHOT_FILE="${SNAPSHOT_FILE:-}"

if [ -n "$SNAPSHOT_FILE" ] && [ -f "$SNAPSHOT_FILE" ]; then
  echo "Using snapshot: $SNAPSHOT_FILE"
  # Extract file paths (newline-separated)
  FILES=$(python3 -c "
import json, sys
manifest = json.load(open(sys.argv[1]))
for f in manifest.get('files', []):
    print(f['path'])
" "$SNAPSHOT_FILE")
else
  echo "No snapshot provided; listing repo tree (non-recursive) for $DATE_FOLDER"
  FILES=$(python3 -c "
from huggingface_hub import HfApi
import os
api = HfApi(token=os.environ.get('HF_TOKEN'))
entries = api.list_repo_tree(repo_id='$REPO_ID', path='$DATE_FOLDER', repo_type='dataset', recursive=False)
for e in sorted(entries, key=lambda x: x.path):
    if not e.path.endswith('/'):
        print(e.path)
  ")
fi