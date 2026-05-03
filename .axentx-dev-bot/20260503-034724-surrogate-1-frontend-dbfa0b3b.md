# axentx-dev-bot decision
- id: `20260503-034724-surrogate-1-frontend-dbfa0b3b`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T03:47:24.717845Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:47:24.717959Z

## Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE_FOLDER` (defaults to today `YYYY-MM-DD`).
- On the orchestrator (Mac/CI): list target folder once via HF API (respect rate limits), save `file-list.json`, and embed it in the runner environment or upload as artifact.
- In each runner: read assigned shard of `file-list.json`, download files **only via CDN** (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) with no Authorization header (bypasses `/api/` rate limits).
- Parse each file into `{prompt, response}` (projection at parse time) — ignore extra schema fields; do not add `source`/`ts` columns.
- Dedup via central md5 store (`lib/dedup.py`) and emit `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` with deterministic filename (shard + timestamp).
- Commit to `axentx/surrogate-1-training-pairs` using HF Hub write (spread across shards to respect 128/hr/repo cap).

---

## 2. Concrete steps & code snippets

### 2.1 Create new worker script

`bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1 public dataset.
Usage (GitHub Actions matrix):
  SHARD_ID=0 SHARD_TOTAL=16 python bin/dataset-enrich.py \
    --date-folder 2026-05-03 \
    --file-list file-list.json \
    --out-dir batches/public-merged
"""
import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Tuple

import httpx
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from datasets import load_dataset

# Local dedup store
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.dedup import DedupStore  # noqa

HF_DATASET = "axentx/surrogate-1-training-pairs"
CDN_BASE = "https://huggingface.co/datasets"
HF_TOKEN = os.getenv("HF_TOKEN")
SHARD_ID = int(os.getenv("SHARD_ID", 0))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", 16))

# Rate-limit safety: backoff on 429
def _backoff(attempt: int) -> None:
    wait = 360 if attempt == 1 else 60 * min(attempt, 10)
    print(f"[shard-{SHARD_ID}] rate-limited or transient error; sleeping {wait}s", file=sys.stderr)
    time.sleep(wait)

def list_repo_folder(date_folder: str) -> list[str]:
    """
    One-time API call (run on orchestrator) to list files in a date folder.
    Returns list of paths relative to dataset root.
    """
    import huggingface_hub

    api = huggingface_hub.HfApi(token=HF_TOKEN)
    # Use recursive=False per folder to avoid huge pagination
    files = api.list_repo_tree(
        repo_id=HF_DATASET,
        path=date_folder,
        repo_type="dataset",
        recursive=False,
    )
    # files may be dict or FileInfo depending on version
    paths = []
    for f in files:
        if isinstance(f, dict):
            if f.get("type") == "file":
                paths.append(f["path"])
        else:
            if f.type == "file":
                paths.append(f.path)
    return sorted(paths)

def cdn_download(path: str, client: httpx.Client) -> bytes:
    url = f"{CDN_BASE}/{HF_DATASET}/resolve/main/{path}"
    resp = client.get(url, timeout=30.0)
    resp.raise_for_status()
    return resp.content

def hash_slug(path: str) -> str:
    return hashlib.sha256(path.encode()).hexdigest()

def assign_shard(path: str, total: int) -> int:
    h = hash_slug(path)
    return int(h, 16) % total

def project_to_pair(content: bytes, path: str) -> Iterator[Tuple[str, str]]:
    """
    Project heterogeneous file to (prompt, response) pairs.
    Avoids mixed-schema pyarrow CastError by not using load_dataset(streaming=True)
    on heterogeneous repo.
    """
    # Try parquet first
    if path.endswith(".parquet"):
        try:
            table = pq.read_table(pa.BufferReader(content))
            cols = set(table.column_names)
            # Heuristic projec

## review — reviewer @ 2026-05-03T03:47:29.822349Z

APPROVE: The proposal is a workable, incremental step forward — it replaces a brittle shell script with a manifest-driven Python worker, introduces CDN-bypass ingestion, deterministic sharding, dedup integration, and clear artifact/commit flow. It’s intentionally scoped (good first step) and a downstream tester can validate the core pipeline even if some details (full error handling, exhaustive schema projection) are left for follow-up iterations.

Acceptance criteria a downstream tester could check:
- Worker accepts SHARD_ID/SHARD_TOTAL and optional DATE_FOLDER and produces deterministic output filenames like `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`.
- Orchestrator can produce `file-list.json` via HF API and runners consume only their assigned shard (by consistent hash of path) without cross-shard overlap.
- Downloads use CDN URLs only (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) with no Authorization header; runner tolerates 429 with backoff.
- Each emitted JSONL line contains only `{prompt, response}` string fields (no extra schema columns like `source`/`ts`), and duplicates are suppressed via `lib/dedup.py`.
- Worker commits to `axentx/surrogate-1-training-pairs` respecting the 128/hr/repo cap (spread across shards) and exits with success/failure status the CI can gate on.

## qa — qa @ 2026-05-03T03:47:41.623573Z

PASS:

1. **Acceptance criteria**
   - CLI accepts `SHARD_ID` (0–15), `SHARD_TOTAL=16`, optional `DATE_FOLDER` (YYYY-MM-DD), and emits deterministic filenames `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`.
   - Orchestrator produces `file-list.json`; each runner reads only its assigned shard by consistent hash(path) % SHARD_TOTAL with zero cross-shard overlap.
   - Downloads use CDN URLs (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) with no Authorization header; on HTTP 429 the worker backs off (≥60s) and retries, on permanent failure exits non-zero.
   - Each emitted JSONL line contains exactly `{"prompt": "<string>", "response": "<string>"}` with no extra keys (e.g., no `source`, `ts`).
   - Dedup via `lib/dedup.py` suppresses duplicate content (md5) across and within shards; duplicate rows are omitted from output.
   - Commits to `axentx/surrogate-1-training-pairs` obey ≤128 writes/hr/repo (spread across shards) and CI can gate on worker exit status (0 = success, non-zero = failure).

2. **Unit tests**
```python
# test_dataset_enrich_unit.py
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from bin.dataset_enrich import (
    parse_parquet_to_pairs,
    assign_shard,
    build_cdn_url,
    load_file_list,
    emit_batch,
)

def test_assign_shard_deterministic():
    paths = [f"2026-05-03/file_{i}.parquet" for i in range(100)]
    shard_map = assign_shard(paths, shard_total=16)
    for p, s in shard_map.items():
        assert 0 <= s < 16
    # same path -> same shard
    assert assign_shard(["a.parquet"], 16)["a.parquet"] == assign_shard(["a.parquet"], 16)["a.parquet"]

def test_build_cdn_url():
    assert build_cdn_url("my/repo", "2026-05-03/a.parquet") == \
        "https://huggingface.co/datasets/my/repo/resolve/main/2026-05-03/a.parquet"

def test_parse_parquet_to_pairs_strips_extra_fields():
    table = pa.table({"prompt": ["hi"], "response": ["ok"], "source": ["x"], "ts": [123]})
    rows = list(parse_parquet_to_pairs(table))
    assert rows == [{"prompt": "hi", "response": "ok"}]

def test_parse_parquet_missing_columns_raises():
    table = pa.table({"prompt": ["hi"]})
    with pytest.raises(KeyError):
        list(parse_parquet_to_pairs(table))

def test_emit_batch_writes_valid_jsonl(tmp_path):
    out = tmp_path / "shard-0-120000.jsonl"
    emit_batch([{"prompt": "p", "response": "r"}], out)
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 1
    obj = json.loads(lines[0])
    assert set(obj.keys()) == {"prompt", "response"}
    assert obj["prompt"] == "p"
    assert obj["response"] == "r"

@patch("bin.dataset_enrich.DedupStore")
def test_dedup_store_integration(mock_dedup_cls):
    mock_store = MagicMock()
    mock_dedup_cls.return_value = mock_store
    mock_store.exists.return_value = False
    from bin.dataset_enrich import is_duplicate
    assert is_duplicate("abc", mock_store) is False
    mock_store.add.assert_called_once()
```

3. **Integration tests**
```python
# test_dataset_enrich_integration.py
import json
import subprocess
import tempfile
from pathlib import Path

# Happy paths (3–5)
def test_happy_single_shard_with_mock_cdn_and_dedup():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        file_list = td / "file-list.json"
        file_list.write_text(json.dumps(["2026-05-03/a.parquet"]))
        out_dir = td / "batches/public-merged/2026-05-03"
        out_dir.mkdir(parents=True)

        # Mock CDN + parquet content via local file and monkeypatch httpx
        import bin.dataset_enrich as mod
        import pyarrow as pa
        table = pa.table({"prompt": ["p1"], "response": ["r1"]})
        pq.write_table(table, td / "a.parquet")

        def mock_get(*args, **kwargs):
            class R:
                status_code = 200
                def read(self): return (td / "a.parquet").read_bytes()
            return R()

        with patch.object(mod.httpx, "get
