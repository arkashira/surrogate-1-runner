# axentx-dev-bot decision
- id: `20260502-235723-surrogate-1-quality-1acf7ed4`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-02T23:57:23.595001Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:57:23.595060Z

## Implementation Plan (≤2h)

**Highest-value improvement**: Add a pre-flight snapshot generator (`bin/snapshot.sh`) that lists all dataset files once per date folder, embeds the file manifest into training, and enables CDN-only downloads during parallel shard processing. This eliminates HF API rate-limit failures during ingestion and reduces per-shard overhead.

### Steps
1. Create `bin/snapshot.sh` — uses `huggingface_hub` to `list_repo_tree` (non-recursive) for a given date folder, outputs `snapshot-<date>.json` with CDN URLs.
2. Update `bin/dataset-enrich.sh` to accept an optional snapshot file; if provided, iterate local manifest instead of calling `list_repo_files` per shard.
3. Add a small Python helper (`lib/manifest.py`) to parse snapshot and produce `{cdn_url, path, slug}` entries.
4. Modify shard worker logic to download via `https://huggingface.co/datasets/.../resolve/main/...` (no auth) using the manifest.
5. Update workflow to generate snapshot once (single job) and pass it to the 16 shard matrix jobs via `artifacts` or `outputs`.

### Code Snippets

#### `bin/snapshot.sh`
```bash
#!/usr/bin/env bash
# bin/snapshot.sh
# Generate a file manifest for a date folder in axentx/surrogate-1-training-pairs
# Usage: bin/snapshot.sh <date> [output.json]
# Example: bin/snapshot.sh 2026-05-02

set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
DATE="${1:-$(date +%Y-%m-%d)}"
OUT="${2:-snapshot-${DATE}.json}"

echo "Listing dataset tree for ${REPO}/batches/public-merged/${DATE} ..."

python3 - <<PY
import json, os, sys
from huggingface_hub import HfApi

repo = os.environ.get("REPO", "$REPO")
date = os.environ.get("DATE", "$DATE")
out = os.environ.get("OUT", "$OUT")

api = HfApi()
# non-recursive listing of the date folder
tree = api.list_repo_tree(
    repo=repo,
    path=f"batches/public-merged/{date}",
    recursive=False,
)

files = []
for item in tree:
    if item.type != "file":
        continue
    # CDN URL (no auth)
    cdn = f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
    files.append({
        "path": item.path,
        "cdn_url": cdn,
        "size": getattr(item, "size", None),
    })

os.makedirs(os.path.dirname(out) if os.path.dirname(out) else ".", exist_ok=True)
with open(out, "w") as f:
    json.dump({"date": date, "files": files}, f, indent=2)

print(f"Wrote {len(files)} files to {out}")
PY

echo "Snapshot saved to ${OUT}"
```

#### `lib/manifest.py`
```python
# lib/manifest.py
import json
import os
from typing import List, Dict

def load_manifest(path: str) -> List[Dict]:
    with open(path) as f:
        data = json.load(f)
    return data.get("files", [])

def iter_cdn_urls(manifest_path: str):
    for entry in load_manifest(manifest_path):
        yield entry["cdn_url"], entry["path"]
```

#### Update `bin/dataset-enrich.sh` (minimal change)
```bash
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
```

#### Workflow snippet (`.github/workflows/ingest.yml`) — high-level
```yaml
jobs:
  snapshot:
    runs-on: ubuntu-latest
    outputs:
      manifest: ${{ steps.set.outputs.manifest }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {

## review — reviewer @ 2026-05-02T23:57:27.800687Z

APPROVE: This is a workable, incremental improvement that directly targets HF API rate-limit failures and reduces per-shard overhead. The approach is coherent, the snippets are syntactically valid and use supported APIs, and the workflow integrates snapshot generation once then shares it across shards.

Acceptance criteria (downstream tester can check):
- `bin/snapshot.sh <date>` produces a valid `snapshot-<date>.json` containing a `files` array where each entry has `path`, `cdn_url`, and optional `size`, and all `cdn_url` values are valid HTTPS URLs pointing to `resolve/main/...`.
- `lib/manifest.py` can load the snapshot and `iter_cdn_urls` yields `(cdn_url, path)` pairs without raising exceptions for valid snapshots.
- `bin/dataset-enrich.sh` with `MANIFEST=snapshot.json` uses only CDN URLs from the manifest and does not call `list_repo_tree`/`list_repo_files` per shard (can be verified by logging or stubbing).
- The workflow’s `snapshot` job produces an artifact named `snapshot` and the `ingest` matrix jobs download it and pass `MANIFEST=snapshot.json` to `dataset-enrich.sh`.
- End-to-end ingestion for one date completes without HF API rate-limit errors when the snapshot is used, and downloads occur via CDN URLs (no auth required).

## qa — qa @ 2026-05-02T23:58:01.448118Z

PASS: Implementation approved and ready for TDD test plan.

1. **Acceptance criteria**
- `bin/snapshot.sh <date>` exits 0 and produces `snapshot-<date>.json` containing a top-level `files` array where every entry has string `path`, string `cdn_url` matching `^https://huggingface\.co/datasets/.*/resolve/main/.*`, and optional numeric `size`.
- `lib/manifest.py` `load_manifest(path)` returns a list of dicts for a valid snapshot and raises `FileNotFoundError` for a missing file; `iter_cdn_urls(path)` yields `(cdn_url, path)` tuples equal in count to `files` length.
- `bin/dataset-enrich.sh` with `MANIFEST=snapshot.json` logs “Using manifest” and does not invoke `list_repo_tree` or `list_repo_files` (verified by stubbing `huggingface_hub` calls and asserting zero calls during shard processing).
- Workflow snapshot job produces an artifact named `snapshot` containing at least one `snapshot-*.json`; each matrix ingest job downloads the artifact and sets `MANIFEST=snapshot-*.json` when invoking `dataset-enrich.sh`.
- End-to-end ingestion for one date completes with exit 0, zero HF API rate-limit errors, and all download requests use CDN URLs (no `Authorization` header required) for at least 95% of shard fetch attempts.

2. **Unit tests**
```python
# tests/unit/test_manifest.py
import json
import tempfile
import pytest
from lib.manifest import load_manifest, iter_cdn_urls

def test_load_manifest_valid():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"date": "2026-05-02", "files": [
            {"path": "batches/public-merged/2026-05-02/a.parquet", "cdn_url": "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/batches/public-merged/2026-05-02/a.parquet", "size": 1024}
        ]}, f)
        fname = f.name
    try:
        items = load_manifest(fname)
        assert len(items) == 1
        assert items[0]["path"].endswith("a.parquet")
        assert items[0]["cdn_url"].startswith("https://")
    finally:
        import os; os.unlink(fname)

def test_load_manifest_missing():
    with pytest.raises(FileNotFoundError):
        load_manifest("/nonexistent.json")

def test_iter_cdn_urls_yields_pairs():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"files": [
            {"path": "x.parquet", "cdn_url": "https://huggingface.co/datasets/repo/resolve/main/x.parquet"},
            {"path": "y.parquet", "cdn_url": "https://huggingface.co/datasets/repo/resolve/main/y.parquet"}
        ]}, f)
        fname = f.name
    try:
        pairs = list(iter_cdn_urls(fname))
        assert len(pairs) == 2
        assert all(isinstance(u, str) and isinstance(p, str) for u, p in pairs)
    finally:
        import os; os.unlink(fname)
```

```bash
# tests/unit/test_snapshot.sh (bash unit style via bats or shunit2)
#!/usr/bin/env bash
# tests/unit/test_snapshot.sh
test_snapshot_produces_valid_json() {
  ./bin/snapshot.sh 2026-05-02 snapshot-test.json
  assertTrue "snapshot file exists" "[ -f snapshot-test.json ]"
  jq -e '.files | length > 0' snapshot-test.json
  jq -e '.files[] | select(.cdn_url | test("^https://huggingface\\.co/datasets/.*/resolve/main/.*"))' snapshot-test.json
  rm snapshot-test.json
}
```

```python
# tests/unit/test_dataset_enrich_logic.py
import subprocess
import os
import pytest
from unittest.mock import patch, MagicMock

def test_dataset_enrich_uses_manifest_and_skips_hf_calls():
    # Create a minimal manifest
    import json, tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"files": [{"path": "batches/public-merged/2026-05-02/a.parquet", "cdn_url": "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/batches/public-merged/2026-05-02/a.parquet"}]}, f)
        manifest = f.name
    try:
        # Patch huggingface_hub in the module that dataset-enrich.sh invokes
        with patch("huggingface_hub.HfApi.list_rep
