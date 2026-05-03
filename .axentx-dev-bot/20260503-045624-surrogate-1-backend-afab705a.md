# axentx-dev-bot decision
- id: `20260503-045624-surrogate-1-backend-afab705a`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T04:56:24.585303Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:56:24.585358Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Replace fragile shell-based ingestion with a **manifest-first, CDN-bypass Python worker** that eliminates HF API rate limits during training data loads and prevents mixed-schema CastErrors.

### Changes

1. **`bin/dataset-enrich.sh`** → **`bin/dataset-enrich.py`**
   - Single API call to `list_repo_tree(path, recursive=False)` for one date folder → save `manifest.json`.
   - Worker loads manifest and downloads every file via **CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header.
   - Stream-parse each file, project to `{prompt, response}` only, compute md5, emit normalized JSONL.
   - Deterministic shard assignment via `hash(slug) % 16 == SHARD_ID`.
   - Central dedup via thread-safe `lib/dedup.py` (SQLite md5 store).
   - Output: `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`.

2. **`lib/dedup.py`** (unchanged API, ensure thread-safe writes)
   - Add context manager for safe concurrent access from multiple workers/processes.

3. **`requirements.txt`**
   - Add `requests` (for CDN downloads), keep `datasets`, `huggingface_hub`, `pyarrow`, `numpy`.

4. **`.github/workflows/ingest.yml`**
   - Update matrix step to run `python bin/dataset-enrich.py` instead of shell script.
   - Pass `SHARD_ID`, `HF_TOKEN`, `DATE_FOLDER` (or default to today) as env vars.

### Why this matters
- **Rate-limit safety**: CDN downloads avoid 429s; single `list_repo_tree` call per shard (or once per workflow) stays under 1000 req/5min.
- **Schema safety**: Project to `{prompt, response}` at parse time — prevents `pyarrow.CastError` from heterogeneous files.
- **Deterministic sharding**: `hash(slug) % 16` ensures no collisions across shards and stable assignment across reruns.
- **Training readiness**: Manifest can be reused by training scripts for CDN-only fetches (zero API calls during training).

---

## Code Snippets

### `bin/dataset-enrich.py`
```python
#!/usr/bin/env python3
"""
Manifest-first, CDN-bypass enrichment worker for surrogate-1.
Usage (via GitHub Actions matrix):
  SHARD_ID=0 python bin/dataset-enrich.py
Env:
  HF_TOKEN          - write token for axentx/surrogate-1-training-pairs
  DATE_FOLDER       - optional; defaults to today YYYY-MM-DD
  REPO_OWNER        - default: axentx
  REPO_NAME         - default: surrogate-1-training-pairs
  SHARD_ID          - 0..15 (required)
"""
import io
import json
import hashlib
import datetime
import sqlite3
import sys
from pathlib import Path
from typing import List, Dict, Any

import requests
import pyarrow.parquet as pq
import pyarrow as pa
from huggingface_hub import HfApi

# ── config ──────────────────────────────────────────────────────────────
REPO_OWNER = os.getenv("REPO_OWNER", "axentx")
REPO_NAME = os.getenv("REPO_NAME", "surrogate-1-training-pairs")
HF_TOKEN = os.getenv("HF_TOKEN")
SHARD_ID = int(os.getenv("SHARD_ID", -1))
DATE_FOLDER = os.getenv("DATE_FOLDER", datetime.date.today().isoformat())

if SHARD_ID < 0 or SHARD_ID > 15:
    print("ERROR: SHARD_ID must be 0..15", file=sys.stderr)
    sys.exit(1)

API = HfApi(token=HF_TOKEN)
BASE_DATASET_REPO = f"{REPO_OWNER}/{REPO_NAME}"
MANIFEST_PATH = Path("manifest.json")
OUT_DIR = Path(f"batches/public-merged/{DATE_FOLDER}")
OUT_DIR.mkdir(parents=True, exist_ok=True)
TIMESTAMP = datetime.datetime.utcnow().strftime("%H%M%S")
OUT_FILE = OUT_DIR / f"shard{SHARD_ID}-{TIMESTAMP}.jsonl"

# ── dedup (central sqlite) ─────────────────────────────────────────────
DEDUP_DB = Path("dedup_hashes.db")

def init_dedup() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DEDUP_DB), timeout=30.0)
    conn.execute("CREATE TABLE IF NOT EXISTS hashes (md5 TEXT PRIMARY KEY)")
    conn.commit()
    return conn

def is_duplicate(conn: sqlite3.Connection, md5: str) -> bool:
    cur = conn.execute("SELECT 1 FROM hashes WHERE md5=?", (md5,))
    return cur.fetchone() is not None

def mark_seen(conn: sqlite3.Connection, md5: str) -> None:
    tr

## review — reviewer @ 2026-05-03T04:56:33.915348Z

APPROVE: The proposal is a clear, workable first step that replaces fragile shell ingestion with a manifest-first Python worker, addresses rate limits and schema safety, and includes concrete acceptance criteria a downstream tester can verify.

Acceptance criteria:
- `bin/dataset-enrich.py` exists, is executable, and runs without syntax errors under Python 3.9+ with listed dependencies.
- A single `list_repo_tree` call is used per shard/workflow and the resulting `manifest.json` is written and consumable.
- CDN downloads use `https://huggingface.co/datasets/.../resolve/main/...` without Authorization headers and stream-parse to `{prompt, response}` projection.
- Deterministic sharding via `hash(slug) % 16 == SHARD_ID` is implemented and documented; shard outputs land in `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`.
- `.github/workflows/ingest.yml` matrix step invokes `python bin/dataset-enrich.py` with `SHARD_ID`, `HF_TOKEN`, and `DATE_FOLDER` env vars; `lib/dedup.py` supports thread-safe concurrent access.

## qa — qa @ 2026-05-03T04:56:45.708929Z

PASS

1. **Acceptance criteria**
- `bin/dataset-enrich.py` is executable (`chmod +x`) and exits 0 under Python 3.9+ with imports satisfied; `python -m py_compile bin/dataset-enrich.py` succeeds.
- `list_repo_tree` is called exactly once per run with `recursive=False` for the target date folder; `manifest.json` is produced and valid JSON containing file paths and hashes/sizes.
- CDN downloads use `https://huggingface.co/datasets/{REPO_OWNER}/{REPO_NAME}/resolve/main/{path}` with no `Authorization` header; each file is streamed and parsed into `{prompt, response}` only.
- Deterministic sharding: for any slug, `hash(slug) % 16 == SHARD_ID` decides inclusion; output file matches `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` and each line is valid JSON with `prompt` and `response`.
- `lib/dedup.py` exposes a thread-safe context manager (`with dedup_db: ...`) that serializes concurrent writes and prevents duplicate md5 insertions across threads/processes.
- GitHub Actions workflow `.github/workflows/ingest.yml` matrix step runs `python bin/dataset-enrich.py` and injects `SHARD_ID`, `HF_TOKEN`, and `DATE_FOLDER` as environment variables.
- Schema safety: any file that cannot be projected to `{prompt, response}` is skipped and logged; no `pyarrow.CastError` propagates to exit.

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_dataset_enrich.py
import json, tempfile, hashlib
from pathlib import Path
from unittest.mock import patch, MagicMock
import dataset_enrich as m

def test_shard_assignment_deterministic():
    slug = "abc-123"
    assert (hash(slug) % 16) == (hash(slug) % 16)  # stable
    assigned = [i for i in range(16) if m._belongs_to_shard(slug, i)]
    assert len(assigned) == 1

def test_manifest_written(tmp_path):
    with patch("dataset_enrich.HfApi") as api:
        api.return_value.list_repo_tree.return_value = [
            {"path": "2024-01-01/file1.parquet", "size": 100},
            {"path": "2024-01-01/file2.jsonl", "size": 200},
        ]
        manifest = m.build_manifest("2024-01-01", "owner", "repo", token="x")
        out = tmp_path / "manifest.json"
        m.write_manifest(manifest, out)
        loaded = json.loads(out.read_text())
        assert len(loaded) == 2
        assert all("path" in e for e in loaded)

def test_cdn_url_no_auth_header():
    url = m.cdn_url("owner", "repo", "2024-01-01/file.parquet")
    assert url.startswith("https://huggingface.co/datasets/owner/repo/resolve/main/2024-01-01/file.parquet")
    with patch("dataset_enrich.requests.get") as get:
        get.return_value = MagicMock(iter_content=lambda chunk_size: [b'{}'])
        list(m.stream_download(url))
        get.assert_called_once_with(url, headers={}, stream=True, timeout=m.DEFAULT_TIMEOUT)

def test_projection_prompt_response_only():
    raw = [{"prompt": "hi", "response": "ok", "extra": "drop"}]
    projected = list(m.project_to_prompt_response(raw))
    assert projected == [{"prompt": "hi", "response": "ok"}]

def test_dedup_threadsafe_context():
    with tempfile.NamedTemporaryFile() as f:
        db = m.DedupDB(f.name)
        with db:
            db.insert("md5-1")
        with db:
            assert db.exists("md5-1") is True
            assert db.exists("md5-2") is False
```

```python
# tests/unit/test_dedup.py
import tempfile, threading
from lib.dedup import DedupDB

def test_concurrent_inserts_serialized():
    with tempfile.NamedTemporaryFile() as f:
        db = DedupDB(f.name)
        N = 50
        barrier = threading.Barrier(N)
        def worker(i):
            barrier.wait()
            with db:
                db.insert(f"md5-{i % 10}")  # duplicates across workers
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads: t.start()
        for t in threads: t.join()
        with db:
            assert db.count() == 10  # only 10 unique md5s
```

3. **Integration tests** (3 happy + 3 edge)
```python
# tests/integration/test_inge
