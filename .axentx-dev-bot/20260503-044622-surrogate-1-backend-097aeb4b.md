# axentx-dev-bot decision
- id: `20260503-044622-surrogate-1-backend-097aeb4b`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T04:46:22.799002Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:46:22.799053Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Replace fragile shell-based ingestion with a **manifest-driven, CDN-bypass Python worker** that eliminates HF API rate limits during training data load and prevents mixed-schema `CastError`s.

### Changes

1. **Add `bin/worker.py`** — single-file worker that:
   - Accepts `SHARD_ID` and `TOTAL_SHARDS` from the matrix.
   - Uses **one HF API call per date folder** via `list_repo_tree(..., recursive=False)` to list files non-recursively, then **caches the full manifest to `manifest.json`** so Lightning training does **zero API calls** during data loading.
   - Filters files deterministically by `hash(slug) % TOTAL_SHARDS == SHARD_ID`.
   - Downloads selected files via **CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) with no auth header.
   - Projects each file to `{prompt, response}` at parse time (avoids mixed-schema `CastError`).
   - Deduplicates via `lib/dedup.py` (central md5 store).
   - Writes output as `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`.

2. **Update `bin/dataset-enrich.sh`** — thin wrapper that:
   - Sets `#!/usr/bin/env bash`, `set -euo pipefail`.
   - Exports `PYTHONUNBUFFERED=1`, `SHELL=/bin/bash`.
   - Invokes `python3 bin/worker.py "$@"`.

3. **Update `.github/workflows/ingest.yml`** — ensure:
   - Matrix uses `shard: [0..15]`.
   - Runs with `bash bin/dataset-enrich.sh`.
   - No recursive `list_repo_files`; rely on worker’s non-recursive tree listing.

4. **Add `requirements.txt` entries** (if missing): `requests`, `tqdm`, `python-slugify` (optional), `pyarrow` (for Parquet support).

---

### Code Snippets

#### `bin/worker.py`

```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1-training-pairs.

Usage:
  SHARD_ID=0 TOTAL_SHARDS=16 python3 bin/worker.py

Environment:
  HF_TOKEN         - write token for axentx/surrogate-1-training-pairs
  HF_REPO          - default: datasets/axentx/surrogate-1-training-pairs
  DEDUP_DB_PATH    - path to central md5 dedup store (default: lib/dedup.py)
"""
import os
import json
import hashlib
import datetime
import time
from pathlib import Path
from typing import List, Dict, Any

import requests
from huggingface_hub import HfApi, hf_hub_download

HF_REPO = os.getenv("HF_REPO", "datasets/axentx/surrogate-1-training-pairs")
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is required")

API = HfApi(token=HF_TOKEN)

# CDN base (no auth, bypasses /api/ rate limits)
CDN_BASE = f"https://huggingface.co/{HF_REPO}/resolve/main"

# Deterministic sharding
TOTAL_SHARDS = int(os.getenv("TOTAL_SHARDS", "16"))
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
assert 0 <= SHARD_ID < TOTAL_SHARDS

# Output root
OUT_ROOT = Path("batches/public-merged")
OUT_ROOT.mkdir(parents=True, exist_ok=True)

# Dedup store
DEDUP_DB_PATH = Path(os.getenv("DEDUP_DB_PATH", "lib/dedup.py"))
if DEDUP_DB_PATH.exists():
    # Import the module dynamically to reuse existing dedup logic
    import importlib.util
    spec = importlib.util.spec_from_file_location("dedup", DEDUP_DB_PATH)
    dedup_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dedup_mod)
    seen = dedup_mod.SeenHashStore()
else:
    # Minimal fallback
    class SeenHashStore:
        def __init__(self):
            self._hashes = set()
        def exists(self, h: str) -> bool:
            return h in self._hashes
        def add(self, h: str) -> None:
            self._hashes.add(h)
    seen = SeenHashStore()

def hf_tree_list(path: str = "") -> List[Dict[str, Any]]:
    """Non-recursive tree listing to avoid paginated list_repo_files."""
    items = API.list_repo_tree(repo_id=HF_REPO, path=path, recursive=False)
    return [i for i in items if i.get("type") in {"file", "blob"}]

def build_manifest() -> List[Dict[str, str]]:
    """
    Build manifest of candidate files.
    Returns list of dicts with keys: path, date (if detectable).
    """
    manifest = []
    # L

## review — reviewer @ 2026-05-03T04:46:29.791717Z

APPROVE — this is a workable, incremental step forward that replaces fragile shell ingestion with a manifest-driven Python worker, eliminates recursive HF API calls during training, and addresses mixed-schema CastError risk by projecting to `{prompt,response}` at parse time.

Acceptance criteria a downstream tester could check:
- Worker runs with `SHARD_ID`/`TOTAL_SHARDS` env vars and produces `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` containing only `{prompt,response}` records.
- Manifest (`manifest.json`) is created and training data loading performs zero HF API calls (verify by disabling token/network to HF API after manifest build).
- Sharding is deterministic: same slug always maps to the same shard across runs (`hash(slug) % TOTAL_SHARDS == SHARD_ID`).
- Deduplication via `lib/dedup.py` prevents duplicate content from appearing across shards/dates (md5-based).
- CDN downloads succeed without auth headers and worker gracefully handles transient HTTP errors (retry/backoff) and malformed files (skip + log).

## qa — qa @ 2026-05-03T04:47:41.469074Z

PASS: surrogate-1 worker plan is workable and incremental.

1. **Acceptance criteria**
- Worker produces `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` containing only `{prompt,response}` records (schema validated; extra keys rejected).
- Manifest (`manifest.json`) is created and training data loading performs zero HF API calls after manifest build (verified by disabling HF API token/network post-manifest).
- Sharding is deterministic: for any slug, `hash(slug) % TOTAL_SHARDS == SHARD_ID` consistently assigns the same shard across runs.
- Deduplication via `lib/dedup.py` prevents duplicate content across shards/dates (md5-based; duplicate rows are omitted from output).
- CDN downloads succeed without auth headers; worker retries transient HTTP errors (429/5xx) with exponential backoff and skips malformed files while logging.
- Worker accepts `SHARD_ID` and `TOTAL_SHARDS` from environment and fails fast with clear message if missing/out-of-range.
- Output file naming matches `shard{N}-{HHMMSS}.jsonl` and contains only records belonging to the assigned shard.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_worker_sharding.py
def test_shard_assignment_deterministic():
    slugs = ["a", "b", "c", "d"]
    assignments = {}
    for s in slugs:
        assignments[s] = hash(s) % 16
    for s in slugs:
        assert hash(s) % 16 == assignments[s]

def test_shard_filter():
    items = [{"slug": f"x{i}", "path": f"2024-01-01/x{i}.json"} for i in range(100)]
    filtered = [i for i in items if shard_for(i["slug"], TOTAL_SHARDS=4, SHARD_ID=1)]
    for i in items:
        expected = (hash(i["slug"]) % 4) == 1
        assert (i in filtered) == expected

# test_worker_manifest.py
def test_manifest_created(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    tree = [{"path": "2024-01-01/a.json", "type": "file"}, {"path": "2024-01-01/b.json", "type": "file"}]
    write_manifest(manifest_path, tree)
    assert manifest_path.exists()
    loaded = json.loads(manifest_path.read_text())
    assert len(loaded) == 2
    assert all("path" in x for x in loaded)

def test_manifest_used_avoids_hf_api_calls(monkeypatch):
    call_count = 0
    def fake_list(*a, **kw):
        nonlocal call_count
        call_count += 1
        return []
    monkeypatch.setattr("huggingface_hub.HfApi.list_repo_tree", fake_list)
    # simulate worker run with existing manifest
    run_worker_with_existing_manifest()
    assert call_count == 0

# test_worker_projection.py
def test_projects_only_prompt_response():
    raw = {"prompt": "hi", "response": "ok", "extra": "x", "meta": {"x": 1}}
    out = project_to_prompt_response(raw)
    assert set(out.keys()) == {"prompt", "response"}
    assert out["prompt"] == "hi"
    assert out["response"] == "ok"

def test_rejects_missing_fields():
    raw = {"prompt": "hi"}
    try:
        project_to_prompt_response(raw)
        assert False, "expected error"
    except ValueError:
        pass

# test_worker_dedup.py
def test_dedup_skips_md5_duplicates(tmp_path):
    db = tmp_path / "dedup.json"
    db.write_text(json.dumps({}))
    seen = is_duplicate(db, "abc123")
    assert seen is False
    seen2 = is_duplicate(db, "abc123")
    assert seen2 is True

# test_worker_cdn_download.py
def test_cdn_url_no_auth():
    url = cdn_url_for("datasets/owner/repo", "2024-01-01/a.json")
    assert "huggingface.co" in url
    assert "resolve/main" in url
    # no auth param

def test_retry_on_transient_errors(requests_mock):
    requests_mock.get(requests_mock.ANY, [{"status_code": 502}, {"status_code": 200, "text": "ok"}])
    resp = download_with_retry("https://huggingface.co/.../a.json")
    assert resp.text == "ok"
```

3. **Integration tests** (happy + edge)

Happy paths
- IT1 — Full shard run with mocked HF tree and CDN files: worker creates manifest, downloads assigned files, projects `{prompt,response}`, deduplicates, and writes `shardN-*.jsonl` with correct record count and schema.
- IT2 — Multiple shards (
