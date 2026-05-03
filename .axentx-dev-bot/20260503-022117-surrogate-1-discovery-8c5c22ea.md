# axentx-dev-bot decision
- id: `20260503-022117-surrogate-1-discovery-8c5c22ea`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T02:21:17.581686Z

## dev — claude/llm-fallback-chain @ 2026-05-03T02:21:17.581737Z

### Final Implementation Plan  
**Goal:** Replace `bin/dataset-enrich.sh` with a robust, manifest-driven, CDN-bypass ingestion worker (`bin/dataset-enrich.py`) that is deterministic, shard-aware, rate-limit-safe, and deployable within 2 hours.

---

### 1. Script Interface and Environment  
Use environment variables (CI-friendly) **and** CLI flags (local/dev-friendly). Resolve contradictions by prioritizing CI usage but supporting both.

```python
#!/usr/bin/env python3
"""
Manifest-driven, CDN-bypass ingestion worker.
Usage (CI):
  SHARD_ID=0 SHARD_TOTAL=16 DATE=2025-01-01 HF_TOKEN=hf_xxx \
    python bin/dataset-enrich.py
Usage (local):
  python bin/dataset-enrich.py --shard_id 0 --shard_total 16 \
    --date 2025-01-01 --hf_token hf_xxx --repo_id axentx/surrogate-1-training-pairs
"""
import argparse
import os
import sys
import json
import hashlib
import logging
from pathlib import Path

import requests
import pyarrow as pa
import pyarrow.parquet as pq
from huggingface_hub import HfApi, hf_hub_download, Repository

# ----------------------------
# Configuration resolution
# ----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Manifest-driven CDN-bypass ingestion worker")
    parser.add_argument("--shard_id", type=int, help="Shard index (0-based)")
    parser.add_argument("--shard_total", type=int, default=16, help="Total shards")
    parser.add_argument("--date", help="Ingestion date (YYYY-MM-DD)")
    parser.add_argument("--hf_token", help="Hugging Face token (write)")
    parser.add_argument("--repo_id", default="axentx/surrogate-1-training-pairs", help="HF dataset repo")
    parser.add_argument("--work_dir", default="/tmp/hf-ingest", help="Working directory")
    parser.add_argument("--manifest_path", help="Optional local manifest JSON for testing")
    return parser.parse_args()

args = parse_args()

# Environment overrides CLI when present (CI behavior)
SHARD_ID = int(os.getenv("SHARD_ID", args.shard_id if args.shard_id is not None else 0))
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", args.shard_total))
DATE = os.getenv("DATE", args.date)
HF_TOKEN = os.getenv("HF_TOKEN", args.hf_token)
REPO_ID = os.getenv("REPO_ID", args.repo_id)
WORK_DIR = Path(os.getenv("WORK_DIR", args.work_dir))
MANIFEST_PATH = os.getenv("MANIFEST_PATH", args.manifest_path)

if not DATE:
    print("ERROR: DATE is required.", file=sys.stderr)
    sys.exit(1)
if not HF_TOKEN:
    print("ERROR: HF_TOKEN is required.", file=sys.stderr)
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
WORK_DIR.mkdir(parents=True, exist_ok=True)
```

---

### 2. Manifest Fetching (CDN-bypass, Rate-Limit Safe)  
Use the Hugging Face **CDN raw file listing via `resolve/main`** for the date prefix. If unavailable, fall back to `huggingface_hub` list_repo_files (slower, API-limited). Prefer CDN.

```python
def fetch_manifest():
    """Return list of parquet filenames for DATE from repo."""
    if MANIFEST_PATH and Path(MANIFEST_PATH).exists():
        logging.info("Using local manifest: %s", MANIFEST_PATH)
        return json.loads(Path(MANIFEST_PATH).read_text())

    # CDN directory listing attempt (common pattern for HF datasets with tree output)
    listing_url = f"https://huggingface.co/{REPO_ID}/tree/main/{DATE}"
    resp = requests.get(listing_url, timeout=30)
    if resp.status_code == 200:
        # Heuristic: parse JSON if returned; otherwise try to parse HTML listing (less reliable)
        try:
            data = resp.json()
            if isinstance(data, list):
                files = [item["path"] for item in data if item.get("type") == "file" and item["path"].endswith(".parquet")]
                if files:
                    logging.info("Fetched manifest via CDN tree JSON: %d files", len(files))
                    return files
        except Exception:
            pass

    # Fallback: use huggingface_hub to list repo files (API-limited)
    try:
        api = 

## review — reviewer @ 2026-05-03T02:22:49.006632Z

APPROVE: Deterministic, manifest-driven worker with CDN-bypass, shard-aware routing, CI+CLI dual interface, and fallback paths is a workable first step; incremental progress that a downstream tester can validate.

Acceptance criteria:
- Script exits non-zero when DATE or HF_TOKEN are missing and logs clear error messages.
- Manifest fetch returns a list of parquet filenames for DATE via CDN JSON when available; falls back to HF API when CDN fails.
- Shard assignment is deterministic: same filename always maps to the same shard index for given SHARD_TOTAL.
- Worker creates WORK_DIR if missing and logs at INFO level with timestamps.
- Local test mode supported via --manifest_path and CLI flags without requiring environment variables.

## qa — qa @ 2026-05-03T02:23:05.402113Z

PASS: Manifest-driven worker plan is testable and deterministic.

1. **Acceptance criteria**
- Exit code 1 and stderr containing “DATE” when DATE is missing.
- Exit code 1 and stderr containing “HF_TOKEN” when HF_TOKEN is missing.
- Manifest fetch returns a non-empty list of parquet filenames for DATE via CDN JSON when available; falls back to HF API when CDN fails (mockable).
- Shard assignment is deterministic: hash(filename) % SHARD_TOTAL produces the same shard index across runs for fixed SHARD_TOTAL.
- Worker creates WORK_DIR if missing (idempotent) and logs at INFO level with ISO-8601-like timestamps.
- Local test mode via --manifest_path and CLI flags works without environment variables (no DATE/HF_TOKEN required when manifest_path is provided and validation is bypassed appropriately).
- No network calls to CDN/HF when a valid local --manifest_path is provided.

2. **Unit tests** (pytest style)
```python
# test_dataset_enrich.py
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import module functions (assume refactored to expose pure functions)
from bin.dataset_enrich import (
    resolve_config,
    fetch_manifest,
    shard_for_filename,
    ensure_work_dir,
)

# ---- resolve_config ----
def test_resolve_config_prioritizes_env_over_cli():
    with patch.dict(os.environ, {"DATE": "2025-01-01", "HF_TOKEN": "hf_env", "SHARD_ID": "3", "SHARD_TOTAL": "8"}):
        cfg = resolve_config(["--date", "2024-01-01", "--hf_token", "hf_cli", "--shard_id", "1", "--shard_total", "4"])
        assert cfg.date == "2025-01-01"
        assert cfg.hf_token == "hf_env"
        assert cfg.shard_id == 3
        assert cfg.shard_total == 8

def test_resolve_config_requires_date():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(SystemExit) as exc:
            resolve_config(["--hf_token", "x"])
        assert exc.value.code == 1

def test_resolve_config_requires_hf_token():
    with patch.dict(os.environ, {"DATE": "2025-01-01"}, clear=True):
        with pytest.raises(SystemExit) as exc:
            resolve_config(["--date", "2025-01-01"])
        assert exc.value.code == 1

def test_resolve_config_local_mode_with_manifest_path():
    cfg = resolve_config(["--manifest_path", "/fake/manifest.json", "--work_dir", "/tmp/test"])
    assert cfg.manifest_path == "/fake/manifest.json"
    assert cfg.work_dir == Path("/tmp/test")

# ---- shard_for_filename ----
def test_shard_for_filename_deterministic():
    filenames = ["a.parquet", "b.parquet", "c.parquet"]
    total = 16
    assignments = [shard_for_filename(f, total) for f in filenames]
    # repeatability
    for f, s in zip(filenames, assignments):
        assert shard_for_filename(f, total) == s
    # distribution sanity
    assert all(0 <= s < total for s in assignments)

# ---- ensure_work_dir ----
def test_ensure_work_dir_creates_if_missing(caplog):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "newdir"
        assert not p.exists()
        ensure_work_dir(p)
        assert p.exists()
    assert "INFO" in caplog.text

# ---- fetch_manifest ----
@patch("bin.dataset_enrich.requests.get")
def test_fetch_manifest_cdn_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"path": "2025-01-01/file1.parquet"},
        {"path": "2025-01-01/file2.parquet"},
    ]
    files = fetch_manifest(date="2025-01-01", repo_id="owner/repo", token="x", use_cdn=True)
    assert files == ["2025-01-01/file1.parquet", "2025-01-01/file2.parquet"]

@patch("bin.dataset_enrich.requests.get")
def test_fetch_manifest_cdn_falls_back_to_hf_api(mock_get):
    mock_get.side_effect = Exception("CDN unreachable")
    with patch("bin.dataset_enrich.HfApi") as MockHfApi:
        mock_api = MagicMock()
        mock_api.list_repo_files.return_value = ["2025-01-01/file1.parquet"]
        MockHfApi.return_value = mock_api
        files = fetch
