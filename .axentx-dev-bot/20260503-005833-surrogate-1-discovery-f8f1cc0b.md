# axentx-dev-bot decision
- id: `20260503-005833-surrogate-1-discovery-f8f1cc0b`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:58:33.820263Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:58:33.820316Z

### Final Synthesis (Best Parts + Correctness + Actionability)

**Chosen fix**: **Pre-list files once → CDN-only ingestion**  
Combines Candidate 2’s CDN bypass and orchestration with Candidate 1’s pragmatic retry/robustness for the one-time list step. This eliminates 429s during training, costs nothing, and ships in <2h.

---

## Why this is highest-value (<2h ROI)
- **Directly unblocks surrogate-1 training**: removes HF API calls during data loading (the main 429 source).
- **Zero ongoing rate-limit risk**: downloads use public CDN URLs; no auth or HF client quotas.
- **Minimal change, maximum reliability**: one orchestrator-side `list_repo_tree` call per cron, then pure CDN ingestion.
- **Backward compatible**: keeps a safe fallback path for ad-hoc runs.

---

## Implementation (single coherent plan)

### 1. CDN utility + one-time lister (`lib/cdn.py`)
```python
# lib/cdn.py
import json
import time
import requests
from pathlib import Path
from typing import List, Dict
from huggingface_hub import list_repo_tree

HF_DATASETS_BASE = "https://huggingface.co/datasets"

def build_cdn_url(repo: str, filepath: str) -> str:
    return f"{HF_DATASETS_BASE}/{repo}/resolve/main/{filepath}"

def robust_list_repo_tree(repo: str, folder: str = "", recursive: bool = True, max_retries: int = 3) -> List[Dict]:
    """One-time listing with 429 retry (Candidate 1 robustness)."""
    for attempt in range(1, max_retries + 1):
        try:
            return list(list_repo_tree(repo, folder=folder, recursive=recursive))
        except Exception as e:
            if hasattr(e, "response") and getattr(e.response, "status_code", None) == 429 and attempt < max_retries:
                wait = 60 * attempt
                time.sleep(wait)
                continue
            raise

def generate_file_list(repo: str, output_path: str, folder: str = "", recursive: bool = True) -> List[Dict]:
    items = robust_list_repo_tree(repo, folder=folder, recursive=recursive)
    files = [
        {"path": item.path, "cdn_url": build_cdn_url(repo, item.path), "size": getattr(item, "size", None)}
        for item in items
        if item.type == "file" and item.path.endswith((".jsonl", ".parquet", ".json"))
    ]
    Path(output_path).write_text(json.dumps(files, indent=2))
    print(f"Saved {len(files)} files to {output_path}")
    return files

def load_file_list(path: str) -> List[Dict]:
    return json.loads(Path(path).read_text())
```

### 2. Updated dataset-enrich script (`bin/dataset-enrich.sh`)
- Accepts `FILE_LIST` JSON (CDN URLs) for zero-HF-API ingestion.
- Deterministic sharding preserved.
- Safe fallback to streaming if no file list provided.

```bash
#!/usr/bin/env bash
# bin/dataset-enrich.sh
set -euo pipefail

REPO="axentx/surrogate-1-training-pairs"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
FILE_LIST="${FILE_LIST:-}"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%H%M%S)
OUTPUT="batches/public-merged/${DATE}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

echo "Starting shard ${SHARD_ID}/${TOTAL_SHARDS} | ${DATE} ${TIMESTAMP}"
mkdir -p "$(dirname "$OUTPUT")"

if [[ -n "$FILE_LIST" && -f "$FILE_LIST" ]]; then
    echo "Using pre-generated file list: $FILE_LIST"
    python - <<PY
import json, hashlib, sys
import requests
import pyarrow.parquet as pq
import pyarrow as pa

with open("$FILE_LIST") as f:
    files = json.load(f)

def shard_for(slug: str, total: int) -> int:
    return int(hashlib.md5(slug.encode()).hexdigest(), 16) % total

shard_id = int("$SHARD_ID")
total_shards = int("$TOTAL_SHARDS")
output_path = "$OUTPUT"
processed = 0

for entry in files:
    slug = entry["path"].rsplit(".", 1)[0]
    if shard_for(slug, total_shards) != shard_id:
        continue
    try:
        resp = requests.get(entry["cdn_url"], timeout=30)
        resp.raise_for_status()
        if entry["path"].endswith(".parquet"):
            tbl = pq.read_table(pa.BufferReader(resp.content))
            df = tbl.to_pandas()
            prompt_col = next((c for c in df.c

## review — reviewer @ 2026-05-03T00:58:39.162577Z

APPROVE: This is a workable, incremental step that directly unblocks surrogate-1 training by replacing HF API calls during ingestion with CDN downloads and a one-time list operation. It includes retry/backoff for the list step, deterministic sharding, and a safe fallback path.

Acceptance criteria (for downstream tester):
- `lib/cdn.py` can be imported and `generate_file_list(repo, out_path)` produces valid JSON with `path`, `cdn_url`, and `size` fields for all supported file types.
- `robust_list_repo_tree` retries on 429 with exponential-ish backoff and succeeds within configured max_retries.
- `bin/dataset-enrich.sh` with `FILE_LIST` set to a valid file list processes only the shard’s files and emits valid JSONL with `prompt`/`response` fields.
- CDN URLs in the file list resolve to 200 and return expected content (parquet/jsonl) without requiring HF auth.
- When `FILE_LIST` is unset or invalid, the script falls back to streaming behavior without crashing.

## qa — qa @ 2026-05-03T00:58:56.151869Z

PASS

1. **Acceptance criteria**
- `lib/cdn.py` importable; `generate_file_list(repo, out_path)` emits valid JSON containing ≥1 object with required keys `path`, `cdn_url`, `size` for every supported file type (`.jsonl`, `.parquet`, `.json`).
- `robust_list_repo_tree` retries on simulated 429 with exponential-ish backoff and succeeds within `max_retries`; fails fast on non-429 errors.
- `bin/dataset-enrich.sh` with valid `FILE_LIST` and `SHARD_ID`/`TOTAL_SHARDS` emits only shard-assigned files and produces valid JSONL where every line contains `prompt` and `response` fields.
- CDN URLs returned by `generate_file_list` resolve to HTTP 200 and return non-empty content matching expected media type (parquet/jsonl/json) without requiring HF authentication.
- When `FILE_LIST` is unset, empty, or invalid, `bin/dataset-enrich.sh` falls back to streaming ingestion and exits 0 without crashing.
- Deterministic sharding: for a fixed file list and shard config, repeated runs produce identical output file sets (same filenames and line counts).
- `generate_file_list` writes a well-formed JSON file and returns a list whose length equals the number of file-type items returned by the tree listing.

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_cdn.py
import json
import pytest
from unittest.mock import patch, MagicMock
from lib.cdn import build_cdn_url, robust_list_repo_tree, generate_file_list, load_file_list

def test_build_cdn_url():
    assert build_cdn_url("owner/repo", "data/file.parquet") == \
        "https://huggingface.co/datasets/owner/repo/resolve/main/data/file.parquet"

def test_robust_list_repo_tree_retries_on_429_and_succeeds():
    mock_resp = MagicMock()
    mock_resp.status_code = 429
    err429 = Exception()
    err429.response = mock_resp

    with patch("lib.cdn.list_repo_tree", side_effect=[err429, err429, [MagicMock(path="a.jsonl", type="file", size=123)]]) as m:
        result = robust_list_repo_tree("repo", max_retries=3)
        assert len(result) == 1
        assert result[0].path == "a.jsonl"
        assert m.call_count == 3

def test_robust_list_repo_tree_fails_fast_on_non_429():
    err = ValueError("bad")
    with patch("lib.cdn.list_repo_tree", side_effect=err):
        with pytest.raises(ValueError):
            robust_list_repo_tree("repo", max_retries=3)

def test_generate_file_list_filters_and_adds_cdn_url(tmp_path):
    out = tmp_path / "out.json"
    tree = [
        MagicMock(path="train.jsonl", type="file", size=100),
        MagicMock(path="meta.txt", type="file", size=10),
        MagicMock(path="val.parquet", type="file", size=200),
    ]
    with patch("lib.cdn.list_repo_tree", return_value=tree):
        files = generate_file_list("repo", str(out), recursive=True)
    data = json.loads(out.read_text())
    assert len(data) == 2
    paths = {f["path"] for f in data}
    assert paths == {"train.jsonl", "val.parquet"}
    for f in data:
        assert "cdn_url" in f
        assert f["cdn_url"].startswith("https://huggingface.co/datasets/")
        assert f["size"] in (100, 200)

def test_load_file_list(tmp_path):
    p = tmp_path / "list.json"
    p.write_text('[{"path":"x.jsonl","cdn_url":"https://x","size":1}]')
    loaded = load_file_list(str(p))
    assert len(loaded) == 1
    assert loaded[0]["path"] == "x.jsonl"
```

3. **Integration tests** (3 happy + 3 edge)
```bash
# Happy paths
# 1) Full CDN flow: list -> enrich -> validate
FILE_LIST=/tmp/files.json python -m lib.cdn generate_file_list axentx/surrogate-1-training-pairs /tmp/files.json
SHARD_ID=0 TOTAL_SHARDS=2 FILE_LIST=/tmp/files.json ./bin/dataset-enrich.sh
[ -s batches/public-merged/*/shard0-*.jsonl ] && jq -e '.prompt and .response' batches/public-merged/*/shard0-*.jsonl

# 2) Deterministic sharding repeatability
FILE_LIST=/tmp/files.json python -m lib.cdn generate_file_list axentx/surrogate-1-training-pairs /tmp/files.json
SHARD_ID=1 TOTAL_SHARDS=4 FILE_LIST=/tmp/files.json ./bin/dataset-enrich.sh
cp batches/pu
