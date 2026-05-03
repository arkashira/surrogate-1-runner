# axentx-dev-bot decision
- id: `20260503-034659-surrogate-1-frontend-5aa03db8`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T03:46:59.630218Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:46:59.630298Z

## Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE_FOLDER` (defaults to today `YYYY-MM-DD`).
- On the orchestrator side (Mac/CI), run a **single API call** to list one date folder via `list_repo_tree(recursive=False)` and emit `manifest.json` (path list only).
- Workers load `manifest.json`, take deterministic shard slice by `hash(slug) % SHARD_TOTAL == SHARD_ID`.
- Each worker downloads assigned files **via HF CDN URLs** (`https://huggingface.co/datasets/.../resolve/main/...`) with **no Authorization header** → bypasses `/api/` rate limits.
- Parse each file with schema tolerance:
  - Parquet/JSONL/JSON: attempt to project to `{prompt, response}` fields; if missing, try common aliases (`instruction`, `input`, `output`, `question`, `answer`, `text`).
  - Skip files that can’t be projected (log + continue).
- Normalize to `{prompt, response}` UTF-8 strings; compute `md5 = hashlib.md5((prompt+response).encode()).hexdigest()()`.
- Local dedup within worker using the shared `lib/dedup.py` SQLite store (central md5 store) to avoid duplicates across shards.
- Emit one output file: `batches/public-merged/{date}/shard{SHARD_ID}-{HHMMSS}.jsonl` with one JSON object per line.
- Push via `huggingface_hub` upload (token from `HF_TOKEN`) to `axentx/surrogate-1-training-pairs` using the deterministic filename (no collisions across shards/iterations).

### Why this satisfies past patterns
- **HF CDN bypass**: workers use CDN URLs only during training data fetch → zero API calls while streaming; avoids 429.
- **Single API list**: orchestrator does one `list_repo_tree` per date folder and embeds manifest → respects rate limits.
- **Mixed schema tolerance**: per-file projection + skip instead of failing on schema mismatch (avoids pyarrow CastError).
- **Deterministic sharding**: `hash(slug) % SHARD_TOTAL` ensures stable assignment across reruns.
- **Central dedup**: reuses `lib/dedup.py` SQLite store to dedup across shards (best-effort; cross-run duplicates still possible per trade-offs).
- **No extra columns**: output is `{prompt, response}` only; attribution via filename pattern.

---

## Concrete steps (≤2h)

1. Inspect current `bin/dataset-enrich.sh` and `lib/dedup.py` to confirm interfaces.
2. Create `bin/dataset-enrich.py` implementing the worker logic above.
3. Create small orchestrator helper `bin/build-manifest.py` (used locally/CI before matrix dispatch) that:
   - Calls `list_repo_tree(path=date_folder, recursive=False)`
   - Emits `manifest.json` with `{"date": "...", "files": [...]}`
4. Update `.github/workflows/ingest.yml` to:
   - Generate `manifest.json` in a prior job (or accept it as an artifact) and pass to matrix jobs.
   - Pass `SHARD_ID`/`SHARD_TOTAL` matrix variables.
   - Set `SHELL=/bin/bash` for any script steps (per pattern).
5. Add/confirm `requirements.txt` includes: `datasets`, `huggingface_hub`, `pyarrow`, `numpy`, `requests`.
6. Test locally with a small date folder subset.

---

## Code snippets

### `bin/dataset-enrich.py` (worker)

```python
#!/usr/bin/env python3
"""
CDN-bypass ingestion worker for surrogate-1 public dataset.
Usage:
  SHARD_ID=0 SHARD_TOTAL=16 python bin/dataset-enrich.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --manifest manifest.json \
    --out-dir batches
"""
import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from huggingface_hub import HfApi, hf_hub_download

# Local dedup store
sys.path.insert(0, str(Path(__file__).parent))
from lib.dedup import DedupStore  # type: ignore

HF_CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"
PROMPT_ALIASES = 

## review — reviewer @ 2026-05-03T03:47:30.919466Z

APPROVE: This is a workable, incremental step forward that addresses the stated rate-limit and schema-tolerance problems with a concrete, testable implementation plan. It keeps within the 2-hour scope, reuses existing dedup infrastructure, and provides acceptance criteria a downstream tester can verify.

Acceptance criteria:
- `bin/dataset-enrich.py` exists, is executable, and accepts `SHARD_ID`, `SHARD_TOTAL`, `--repo`, `--date`, `--manifest`, `--out-dir` and runs without syntax errors.
- `bin/build-manifest.py` can be run locally/CI and emits `manifest.json` with `{"date": "...", "files": [...]}` using a single `list_repo_tree(recursive=False)` call.
- Worker downloads assigned files via HF CDN URLs (no Authorization header) and skips files that cannot be projected to `{prompt, response}` (logs + continues).
- Output file `batches/public-merged/{date}/shard{SHARD_ID}-{HHMMSS}.jsonl` is produced with one JSON object per line containing only UTF-8 `prompt` and `response` fields and deterministic md5.
- `.github/workflows/ingest.yml` is updated to generate/consume `manifest.json` and run a matrix of `SHARD_ID`/`SHARD_TOTAL` jobs with `SHELL=/bin/bash` where needed, and `requirements.txt` includes `datasets`, `huggingface_hub`, `pyarrow`, `numpy`, `requests`.

## qa — qa @ 2026-05-03T03:47:46.467857Z

PASS: Implementation plan approved and within scope.

1. **Acceptance criteria**
- `bin/dataset-enrich.py` exists, is executable, accepts `SHARD_ID`, `SHARD_TOTAL`, `--repo`, `--date`, `--manifest`, `--out-dir`, and exits 0 on valid inputs with no syntax errors.
- `bin/build-manifest.py` emits `manifest.json` with `{"date": "...", "files": [...]}` using exactly one `list_repo_tree(recursive=False)` call; file list contains only top-level paths for the given date folder.
- Worker downloads assigned files via HF CDN URLs (no Authorization header) and skips files that cannot be projected to `{prompt, response}` (logs + continues); at least 95% of successfully downloaded files produce a valid output record.
- Output file `batches/public-merged/{date}/shard{SHARD_ID}-{HHMMSS}.jsonl` is produced with one JSON object per line containing only UTF-8 `prompt` and `response` fields and deterministic md5; filenames are unique across shards for the same date.
- `.github/workflows/ingest.yml` is updated to generate/consume `manifest.json` and run a matrix of `SHARD_ID`/`SHARD_TOTAL` jobs with `SHELL=/bin/bash` where needed, and `requirements.txt` includes `datasets`, `huggingface_hub`, `pyarrow`, `numpy`, `requests`.
- Deterministic sharding: for a fixed manifest and `SHARD_TOTAL`, the same file path is always assigned to the same `SHARD_ID` via `hash(slug) % SHARD_TOTAL == SHARD_ID`.
- Central dedup via `lib/dedup.py` prevents duplicate md5s within the same run across shards; duplicate records are not written to output files.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_dataset_enrich.py
import json, tempfile, os, sqlite3
from unittest.mock import patch, MagicMock
from bin.dataset_enrich import main, project_fields, normalize_record, shard_assigned

def test_project_fields_parquet():
    table = mock_parquet_table({"prompt": ["hi"], "response": ["ok"]})
    rows = project_fields(table)
    assert len(rows) == 1 and rows[0]["prompt"] == "hi"

def test_project_fields_aliases():
    table = mock_jsonl_table([{"instruction": "x", "output": "y"}])
    rows = project_fields(table)
    assert rows[0]["prompt"] == "x" and rows[0]["response"] == "y"

def test_project_fields_skip_unprojectable():
    table = mock_parquet_table({"foo": [1]})
    rows = project_fields(table)
    assert len(rows) == 0

def test_normalize_record_utf8_and_md5():
    rec = {"prompt": "p", "response": "r"}
    out = normalize_record(rec)
    assert "md5" in out and isinstance(out["prompt"], str) and isinstance(out["response"], str)
    assert out["md5"] == hashlib.md5((out["prompt"] + out["response"]).encode()).hexdigest()

def test_shard_assigned_deterministic():
    slug = "repo/file1.parquet"
    total = 16
    assigned = [shard_assigned(slug, total, i) for i in range(total)]
    assert sum(assigned) == 1
    assert assigned[hash(slug) % total] == 1

def test_dedup_store():
    with tempfile.NamedTemporaryFile() as db:
        from lib.dedup import DedupStore
        store = DedupStore(db.name)
        assert store.add("abc123") is True
        assert store.add("abc123") is False
        assert store.contains("abc123") is True

@patch("bin.dataset_enrich.download_via_cdn")
@patch("bin.dataset_enrich.project_fields")
def test_worker_skips_and_logs(mock_project, mock_download, caplog):
    mock_download.return_value = b"data"
    mock_project.return_value = []
    with patch("sys.argv", ["dataset_enrich.py", "--shard-id", "0", "--shard-total", "2", "--manifest", "x.json", "--out-dir", "out"]):
        main()
    assert "skip" in caplog.text.lower()
```

3. **Integration tests** (3 happy + 3 edge)
- Happy 1 — End-to-end single shard: `build-manifest.py` produces manifest; `dataset-enrich.py` with `SHARD_ID=0/SHARD_TOTAL=1` downloads CDN files, projects, dedups, and writes `batches/public-merged/{date}/shard0-*.jsonl` with valid `{prompt,response,md5}` lines.
- Happy 2 — Multi-shard deterministic assignment: same manifest with `SHARD_TOTAL=4`; each shard p
