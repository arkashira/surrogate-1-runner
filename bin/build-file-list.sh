#!/usr/bin/env bash
set -euo pipefail
# Usage: RUN_DATE=YYYY-MM-DD ./bin/build-file-list.sh
# Produces: file-list.json  (JSON object with date + files array)

: "${HF_TOKEN:?}"
: "${RUN_DATE:=$(date -u +%Y-%m-%d)}"

REPO="datasets/axentx/surrogate-1-training-pairs"

python -c "
import json, os, datetime, sys
from huggingface_hub import HfApi
api = HfApi(token=os.getenv('HF_TOKEN'))
repo = 'datasets/axentx/surrogate-1-training-pairs'
today = os.getenv('RUN_DATE', datetime.datetime.utcnow().strftime('%Y-%m-%d'))
files = [f.rfilename for f in api.list_repo_tree(repo, path=today, recursive=False)]
out = {'date': today, 'files': sorted(files)}
with open('file-list.json', 'w') as f:
    json.dump(out, f, indent=2)
print(json.dumps(out))
"