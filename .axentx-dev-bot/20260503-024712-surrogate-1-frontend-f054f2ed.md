# axentx-dev-bot decision
- id: `20260503-024712-surrogate-1-frontend-f054f2ed`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T02:47:12.812187Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:47:12.812270Z

## Final Implementation Plan (≤2 h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that is safe for GitHub Actions matrix (16 shards), deterministic, and zero-training-API-pressure.

### Core behavior (merged + resolved)
- **Inputs**: `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN` (optional for write), `HF_REPO` (default `datasets/axentx/surrogate-1-training-pairs`), optional `--manifest-file`.
- **Listing**: one `list_repo_tree(path=DATE, recursive=False)` (or cached manifest) to enumerate files in `DATE/`. Deterministic shard assignment via `hash(slug) % SHARD_TOTAL`.
- **Download**: CDN-only (`https://huggingface.co/datasets/.../resolve/main/...`). No Authorization header for downloads (zero API rate-limit pressure). If repo is private, use token only for listing/upload; downloads still via CDN with token-in-URL only when strictly required (kept explicit).
- **Parsing**: stream each file and project to `{prompt, response}` at parse time. Do **not** rely on `load_dataset(streaming=True)` on heterogeneous schemas (avoids mixed-schema failures). Implement per-format lightweight streaming readers (JSONL, JSON, Parquet via `pyarrow`/`pandas` chunks) with a small, explicit projection layer.
- **Deduplication**: central md5 store (`lib/dedup.py`) before emitting.
- **Output**: newline-delimited JSON to `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`. Optional upload: one commit per shard per run via HF API.
- **Exit**: clear status codes and structured logs; safe for CI matrix.

Time budget: ~90 minutes (60m implementation + 30m smoke test).

---

## Changes

### 1) Create `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.

Usage (local):
  DATE=2026-05-03 SHARD_ID=0 SHARD_TOTAL=16 \
  HF_TOKEN=hf_xxx \
  python bin/dataset-enrich.py

Usage (CI):
  python bin/dataset-enrich.py \
    --shard-id "$SHARD_ID" \
    --shard-total "$SHARD_TOTAL" \
    --date "$DATE" \
    --hf-token "$HF_TOKEN" \
    --hf-repo "datasets/axentx/surrogate-1-training-pairs" \
    --manifest-file manifest.json

If --manifest-file is provided, skip list_repo_tree and use that list.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import requests
from huggingface_hub import HfApi, list_repo_tree

# Project-local dedup store
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.dedup import DedupStore  # type: ignore

HF_REPO_DEFAULT = "datasets/axentx/surrogate-1-training-pairs"
CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"
BATCH_DIR_TEMPLATE = "batches/public-merged/{date}"

# Deterministic shard assignment
def shard_for_slug(slug: str, shard_total: int) -> int:
    digest = hashlib.md5(slug.encode("utf-8")).hexdigest()
    return int(digest, 16) % shard_total

def build_file_list_api(date: str, repo: str, hf_token: Optional[str]) -> List[str]:
    """
    Single API call: list files in DATE folder (non-recursive).
    Returns list of repo-relative paths.
    """
    try:
        items = list_repo_tree(
            repo_id=repo,
            path=date,
            repo_type="dataset",
            token=hf_token,
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to list repo tree for {repo}/{date}: {exc}") from exc

    paths = [it["path"] for it in items if it.get("type") == "file"]
    if not paths:
        print(f"[WARN] No files found in {repo}/{date}", file=sys.stderr)
    return paths

def build_file_list_manifest(manifest_path: Path) -> List[str]:
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "files" in data:
        return data["files"]
    if isinstance(data, list):
        return data
    raise ValueError(f"Inva

## review — reviewer @ 2026-05-03T02:47:17.397235Z

APPROVE: This is a workable, incremental step forward that replaces shell-based brittle ingestion with a manifest-driven, CDN-bypass worker safe for GitHub Actions matrix. It addresses determinism, rate-limit pressure, and schema heterogeneity with explicit per-format streaming readers and deduplication. Downstream testers can verify shard assignment, CDN-only downloads, and output batches.

Acceptance criteria:
- Script accepts `SHARD_ID`, `SHARD_TOTAL`, `DATE`, optional `HF_TOKEN`/`--manifest-file`, and produces newline-delimited JSON under `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`.
- Deterministic shard assignment uses `hash(slug) % SHARD_TOTAL` and matches across runs for same inputs.
- Downloads use CDN URLs without Authorization headers (token only for listing/upload when repo is private); failures on private repos without token are graceful and logged.
- Per-format streaming readers (JSONL, JSON, Parquet) project to `{prompt, response}` and skip malformed lines without crashing the worker.
- Dedup store (`lib/dedup.py`) is imported and consulted before emitting records; duplicates are skipped and counted in logs.
- Exit codes and structured logs are clear for CI matrix (0 on success, non-zero on fatal errors; warnings to stderr).

## qa — qa @ 2026-05-03T02:47:59.652578Z

PASS: Ready for TDD plan.

1. **Acceptance criteria**
- Script accepts `SHARD_ID`, `SHARD_TOTAL`, `DATE`, optional `HF_TOKEN`/`--manifest-file`, and produces newline-delimited JSON under `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl` with ≥1 record when input exists.
- Deterministic shard assignment uses `hash(slug) % SHARD_TOTAL` and produces identical shard index across runs for same slug and shard total (16).
- Downloads use CDN URLs without Authorization headers; token is used only for listing/upload when repo is private; private-repo attempts without token produce graceful error logs and non-zero exit.
- Per-format streaming readers (JSONL, JSON, Parquet) project to `{prompt, response}` and skip malformed lines without crashing; success rate ≥95% on valid lines in mixed files.
- Dedup store (`lib/dedup.py`) is consulted before emitting; duplicate records are skipped and counted in logs; emitted record count + duplicate count equals total parsed records.
- Exit codes and structured logs are CI-friendly: exit 0 on success, non-zero on fatal errors; warnings/errors written to stderr with timestamp and component tag.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_shard_for_slug.py
def test_shard_for_slug_deterministic():
    assert shard_for_slug("a/b/file.jsonl", 16) == shard_for_slug("a/b/file.jsonl", 16)

def test_shard_for_slug_uniform():
    slugs = [f"file-{i}.jsonl" for i in range(1000)]
    assignments = [shard_for_slug(s, 16) for s in slugs]
    assert all(0 <= a < 16 for a in assignments)

# test_cdn_url.py
def test_cdn_url_no_auth():
    url = cdn_url("datasets/axentx/surrogate-1-training-pairs", "2026-05-03/file.jsonl")
    assert "huggingface.co/datasets" in url
    assert "authorization" not in url.lower()

# test_streaming_readers.py
def test_jsonl_projector(tmp_path):
    f = tmp_path / "x.jsonl"
    f.write_text('{"prompt":"hi","response":"ok"}\n{"prompt":"bad"}\n')
    records = list(stream_jsonl(f, projection=["prompt", "response"]))
    assert len(records) == 1
    assert records[0]["prompt"] == "hi"
    assert records[0]["response"] == "ok"

def test_json_projector(tmp_path):
    f = tmp_path / "x.json"
    f.write_text('[{"prompt":"a","response":"b"}]')
    records = list(stream_json(f, projection=["prompt", "response"]))
    assert len(records) == 1

def test_parquet_projector(tmp_path):
    import pyarrow as pa, pyarrow.parquet as pq
    tbl = pa.table({"prompt": ["x"], "response": ["y"], "extra": [1]})
    f = tmp_path / "x.parquet"
    pq.write_table(tbl, f)
    records = list(stream_parquet(f, projection=["prompt", "response"]))
    assert len(records) == 1
    assert "extra" not in records[0]

# test_dedup_integration_unit.py
def test_dedup_store_skips_duplicates(tmp_path):
    store = DedupStore(tmp_path / "dedup.db")
    r = {"prompt": "p", "response": "r"}
    assert not store.has(r)
    store.add(r)
    assert store.has(r)

# test_cli_args.py
def test_parser_required():
    args = parse_args(["--shard-id", "0", "--shard-total", "16", "--date", "2026-05-03"])
    assert args.shard_id == 0
    assert args.shard_total == 16
    assert args.date == "2026-05-03"
    assert args.manifest_file is None
```

3. **Integration tests** (3 happy + 3 edge)
```python
# Happy paths
def test_happy_public_repo_cdn_only(tmp_path, mocker):
    # Mock list_repo_tree -> one file; mock CDN download -> valid JSONL
    # Run worker with SHARD_TOTAL=16, SHARD_ID=0
    # Assert: output file exists, records contain {prompt,response}, no auth header used
    pass

def test_happy_manifest_mode(tmp_path, mocker):
    # Provide --manifest-file listing one file; mock CDN download -> valid Parquet
    # Assert: list_repo_tree not called; output produced; dedup consulted
    pass

def test_happy_upload_shard(tmp_path, mocker):
    # With HF_TOKEN, mock upload via HfApi.create_commit
    # Assert: one commit created with correct files; exit 0
    pass

# Edge cases
def test_edge_private_repo_no_token(tmp_p
