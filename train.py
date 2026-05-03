# Generate manifest for one partition
python tools/snapshot_manifest.py \
  --repo axentx/surrogate-1-training-pairs \
  --date 2026-04-29 \
  --out file_manifest.json

# Dry-run: verify manifest + CDN fetch for a small sample
python -c "
import json, sys
from train import load_cdn_parquet

with open('file_manifest.json') as f:
    m = json.load(f)

sample = m['files'][0]['cdn_url']
rows = load_cdn_parquet(sample, columns=['prompt', 'response'])
assert len(rows) > 0, 'No rows fetched'
assert all('prompt' in r and 'response' in r for r in rows), 'Schema mismatch'
print('OK: manifest + CDN fetch works')
"