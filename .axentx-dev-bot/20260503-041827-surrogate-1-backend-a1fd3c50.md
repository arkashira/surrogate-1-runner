# axentx-dev-bot decision
- id: `20260503-041827-surrogate-1-backend-a1fd3c50`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T04:18:27.553318Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:18:27.553396Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Replace fragile shell-based ingestion with a **manifest-driven, CDN-bypass Python worker** that eliminates HF API rate limits during training data loads and prevents mixed-schema CastErrors.

### Changes

1. Add `bin/worker.py` — single-file, manifest-driven worker that:
   - Accepts `SHARD_ID` and `TOTAL_SHARDS` (matrix) and a date folder (via `--date` or env).
   - Uses one HF API call (`list_repo_tree`) to list the target date folder, saves `manifest.json`.
   - Downloads only assigned shard files via **CDN bypass** (`resolve/main/...` with no auth).
   - Projects heterogeneous files to `{prompt, response}` at parse time (avoids `load_dataset`/pyarrow CastError).
   - Deduplicates via centralized SQLite md5 store (`lib/dedup.py`).
   - Streams output to `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`.
   - Exits 0 on success, non-zero on failure (GitHub Actions friendly).

2. Update `bin/dataset-enrich.sh` → thin wrapper that:
   - Sets `#!/usr/bin/env bash`, `set -euo pipefail`.
   - Exports `PYTHONUNBUFFERED=1`, `SHELL=/bin/bash`.
   - Invokes `python3 bin/worker.py` with matrix args.

3. Update `.github/workflows/ingest.yml` to:
   - Pass `date` (default: today) and matrix `shard_id`/`total_shards`.
   - Use `actions/setup-python` (3.10+).
   - Cache pip deps for speed.

4. Add minimal `requirements.txt` update (if missing): `requests`, `tqdm`, `pyarrow` (for parquet fallback).

---

### Code Snippets

#### `bin/worker.py`

```python
#!/usr/bin/env python3
"""
Manifest-driven, CDN-bypass ingestion worker.

Usage:
  SHARD_ID=0 TOTAL_SHARDS=16 python bin/worker.py --repo axentx/surrogate-1-training-pairs --date 2026-05-03
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

import requests
from tqdm import tqdm

HF_API = "https://huggingface.co/api"
CDN = "https://huggingface.co/datasets"
RETRY_WAIT = 360  # on 429

# ── dedup store ──────────────────────────────────────────────────────────────

def _get_db_path() -> Path:
    # Keep existing convention: central store on HF Space would be /data/dedup.db
    # For GitHub runners we use a local file (ephemeral). Cross-run dedup remains
    # best-effort; source-of-truth is the HF Space.
    return Path(os.getenv("DEDUP_DB", "dedup.db"))

def already_seen(digest: str) -> bool:
    import sqlite3

    db = _get_db_path()
    db.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(db)) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS seen (md5 TEXT PRIMARY KEY)")
        cur = conn.execute("SELECT 1 FROM seen WHERE md5=?", (digest,))
        return cur.fetchone() is not None

def mark_seen(digest: str) -> None:
    import sqlite3

    db = _get_db_path()
    with sqlite3.connect(str(db)) as conn:
        conn.execute("INSERT OR IGNORE INTO seen (md5) VALUES (?)", (digest,))

# ── HF helpers ───────────────────────────────────────────────────────────────

def list_date_folder(repo: str, date: str) -> List[Dict[str, Any]]:
    """Single API call to list files in {date}/ (non-recursive)."""
    url = f"{HF_API}/datasets/{repo}/tree/main/{date}"
    r = requests.get(url, timeout=30)
    if r.status_code == 429:
        print(f"Rate limited. Waiting {RETRY_WAIT}s", file=sys.stderr)
        time.sleep(RETRY_WAIT)
        return list_date_folder(repo, date)
    r.raise_for_status()
    return r.json()

def cdn_download(repo: str, path: str, dest: Path) -> None:
    """Download via CDN (no auth)."""
    url = f"{CDN}/{repo}/resolve/main/{path}"
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

# ── projection (schema-agnostic) ────────────────────────────────────────────

def project_to_pair(raw: Dict[str, Any]) 

## review — reviewer @ 2026-05-03T04:18:31.110966Z

APPROVE: Manifest-driven worker is a clear, incremental improvement that directly addresses HF rate limits and CastErrors; the design is concrete, GitHub Actions–ready, and testable.

Acceptance criteria:
- Worker accepts `SHARD_ID`, `TOTAL_SHARDS`, and `--date` (or env) and exits 0 on success / non-zero on failure.
- Single `list_repo_tree` API call produces `manifest.json`; shard assignment is deterministic from filename list.
- Downloads use CDN bypass (`resolve/main/...`) without auth; 429 triggers exponential backoff/retry (≥360s initial wait).
- Projection function maps heterogeneous source files to `{prompt, response}` and never raises on missing keys; malformed rows are logged/skipped rather than crashing.
- Dedup via SQLite `seen(md5)` is idempotent and uses `INSERT OR IGNORE`; output written to `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` as newline-delimited JSON.

## qa — qa @ 2026-05-03T04:18:59.965838Z

PASS: 

### 1. Acceptance criteria
* The worker accepts `SHARD_ID`, `TOTAL_SHARDS`, and `--date` (or env) and exits 0 on success.
* The worker exits non-zero on failure.
* A single `list_repo_tree` API call produces `manifest.json`.
* Shard assignment is deterministic from filename list.
* Downloads use CDN bypass (`resolve/main/...`) without auth.
* 429 triggers exponential backoff/retry (≥360s initial wait).
* Projection function maps heterogeneous source files to `{prompt, response}` without raising on missing keys.
* Malformed rows are logged/skipped rather than crashing.
* Dedup via SQLite `seen(md5)` is idempotent and uses `INSERT OR IGNORE`.
* Output is written to `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` as newline-delimited JSON.

### 2. Unit tests
```python
import unittest
from unittest.mock import patch, MagicMock
from bin.worker import already_seen, mark_seen, _get_db_path

class TestWorker(unittest.TestCase):
    @patch('sqlite3.connect')
    def test_already_seen(self, mock_connect):
        mock_connect.return_value.cursor().fetchone.return_value = None
        self.assertFalse(already_seen('digest'))
        mock_connect.return_value.cursor().fetchone.return_value = (1,)
        self.assertTrue(already_seen('digest'))

    @patch('sqlite3.connect')
    def test_mark_seen(self, mock_connect):
        mark_seen('digest')
        mock_connect.return_value.cursor().execute.assert_called_with("INSERT OR IGNORE INTO seen (md5) VALUES (?)", ('digest',))

    def test_get_db_path(self):
        self.assertEqual(_get_db_path(), Path('dedup.db'))
        with patch.dict('os.environ', {'DEDUP_DB': '/path/to/db'}):
            self.assertEqual(_get_db_path(), Path('/path/to/db'))

if __name__ == '__main__':
    unittest.main()
```

### 3. Integration tests
Happy paths:
1. Test successful ingestion with valid `SHARD_ID`, `TOTAL_SHARDS`, and `--date`.
2. Test successful ingestion with valid `SHARD_ID`, `TOTAL_SHARDS`, and env `DATE`.
3. Test successful retry after 429 error.
Edge cases:
1. Test failure with invalid `SHARD_ID`.
2. Test failure with invalid `TOTAL_SHARDS`.
3. Test failure with missing `--date` and env `DATE`.

Example integration test:
```python
import subprocess
import os
import time

def test_successful_ingestion():
    # Set up valid SHARD_ID, TOTAL_SHARDS, and --date
    shard_id = 0
    total_shards = 16
    date = '2026-05-03'
    # Run worker
    subprocess.run(['python', 'bin/worker.py', '--repo', 'axentx/surrogate-1-training-pairs', '--date', date, 'SHARD_ID={}'.format(shard_id), 'TOTAL_SHARDS={}'.format(total_shards)], check=True)
    # Check output
    output_file = 'batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl'.format(date=date, N=shard_id, HHMMSS=int(time.time()))
    assert os.path.exists(output_file)

def test_retry_after_429():
    # Set up valid SHARD_ID, TOTAL_SHARDS, and --date
    shard_id = 0
    total_shards = 16
    date = '2026-05-03'
    # Mock 429 error
    with patch('requests.get') as mock_get:
        mock_get.side_effect = [MagicMock(status_code=429), MagicMock(status_code=200)]
        # Run worker
        subprocess.run(['python', 'bin/worker.py', '--repo', 'axentx/surrogate-1-training-pairs', '--date', date, 'SHARD_ID={}'.format(shard_id), 'TOTAL_SHARDS={}'.format(total_shards)], check=True)
        # Check output
        output_file = 'batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl'.format(date=date, N=shard_id, HHMMSS=int(time.time()))
        assert os.path.exists(output_file)
```

### 4. Risk register
* **Risk**: Worker fails to handle large number of files in a shard.
	+ **Detection**: Monitor worker logs for errors related to file handling.
	+ **Mitigation**: Increase resources allocated to worker or optimize file handling code.
* **Risk**: Worker fails to retry after 429 error.
	+ **Detection**: Monitor worker logs for errors related to 429 errors.
	+ **Mitigation**: Increase retry wait time or optimize retry logic.
* **Risk**: Worker fails to 
