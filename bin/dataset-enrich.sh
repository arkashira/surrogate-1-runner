# Near top of dataset-enrich.sh, after argument parsing
MANIFEST="${MANIFEST:-}"
if [ -n "${MANIFEST}" ] && [ -f "${MANIFEST}" ]; then
  echo "Using manifest ${MANIFEST}"
  # Use python helper to stream CDN URLs instead of HF API listing
  URLS=$(python3 -c "
import sys, json
with open('${MANIFEST}') as f:
    files = json.load(f).get('files', [])
for f in files:
    print(f['cdn_url'])
")
else
  # fallback to existing behavior (HF API listing)
  URLS=$(python3 -c "
from huggingface_hub import HfApi
api = HfApi()
tree = api.list_repo_tree('axentx/surrogate-1-training-pairs', path='batches/public-merged/${DATE}', recursive=False)
for item in tree:
    if item.type == 'file':
        print(f'https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{item.path}')
")
fi

# Then iterate over $URLS as before (download via CDN URLs)