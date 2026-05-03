# axentx-dev-bot decision
- id: `20260503-015852-surrogate-1-quality-bacfceb6`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T01:58:52.586094Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:58:52.586191Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID` and `SHARD_TOTAL` (16) from the GitHub Actions matrix.
- Loads a pre-generated `manifest-YYYYMMDD.json` (created once per run by a lightweight Mac/CI step) containing the list of files to process for the target date folder.
- Assigns files to shards deterministically via `hash(slug) % SHARD_TOTAL`.
- Downloads assigned files via **HF CDN bypass** (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header.
- Projects each file to `{prompt, response}` only at parse time (avoids mixed-schema `pyarrow.CastError`).
- Deduplicates via the existing central md5 store (`lib/dedup.py`).
- Writes output to `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` (one file per shard per run).
- Exits with success/failure codes so GitHub Actions can retry cleanly.

### Steps (≤2h)

1. Create `bin/dataset-enrich.py` (replaces `bin/dataset-enrich.sh`).
2. Add `bin/gen-manifest.py` (optional helper; can also be run in CI once per cron tick).
3. Update `.github/workflows/ingest.yml` to:
   - Generate or fetch `manifest-YYYYMMDD.json` once (e.g., via a `setup` job or inline step using `gh api` + `jq`).
   - Pass manifest path to each matrix shard via env.
   - Use `bash` explicitly and ensure scripts are executable.
4. Ensure `lib/dedup.py` is importable and thread-safe for parallel shard runs.
5. Test locally with a small manifest subset.

---

## bin/dataset-enrich.py

```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.

Usage (GH Actions matrix):
  SHARD_ID=0 SHARD_TOTAL=16 \
  MANIFEST_PATH=manifest-20260503.json \
  python bin/dataset-enrich.py

Environment:
  HF_DATASET_REPO   (default: axentx/surrogate-1-training-pairs)
  HF_TOKEN          (optional; not used for CDN downloads)
  DATE_FOLDER       (e.g., 2026-05-03)
  OUT_DIR           (default: ./batches/public-merged)
"""

import json
import hashlib
import os
import sys
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

import requests
import pyarrow.parquet as pq
import pyarrow as pa

# Local dedup store
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.dedup import DedupStore  # type: ignore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [shard%(shard)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

CDN_BASE = "https://huggingface.co/datasets"
DEFAULT_REPO = "axentx/surrogate-1-training-pairs"

def slug_for_path(path: str) -> str:
    """Stable slug for dedup/sharding (no extension)."""
    return path.rsplit(".", 1)[0].replace("/", "-")

def shard_assign(slug: str, total: int) -> int:
    """Deterministic shard assignment."""
    digest = hashlib.md5(slug.encode()).hexdigest()
    return int(digest, 16) % total

def cdn_download(url: str, timeout: int = 30) -> bytes:
    """Download via HF CDN (no auth)."""
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.content

def project_to_pair(raw: Dict[str, Any], path: str) -> Dict[str, Any]:
    """
    Project heterogeneous file to {prompt, response} only.
    Add minimal attribution via filename pattern (no source/ts cols).
    """
    prompt = raw.get("prompt") or raw.get("input") or raw.get("question") or ""
    response = raw.get("response") or raw.get("output") or raw.get("answer") or ""

    # If nested (e.g., messages), attempt simple flatten
    if not prompt and isinstance(raw.get("messages"), list):
        msgs = raw["messages"]
        prompts = [m.get("content", "") for m in msgs if m.get("role") in ("user", "human")]
        responses = [m.get("content", "") for m in msgs if m.get("role") in ("assistant", "bot", "system")]
        prompt = " ".join(prompts)
        response = " ".join(responses)

    return {
        "prompt": str(p

## review — reviewer @ 2026-05-03T01:58:57.936083Z

APPROVE: The PR introduces a clear, incremental improvement by replacing a brittle shell script with a manifest-driven Python worker that avoids mixed-schema errors and supports deterministic sharding and CDN-bypass downloads; it provides a workable path to reliable ingestion and leaves room for iteration.

Acceptance criteria:
- `bin/dataset-enrich.py` must parse and run without syntax errors and accept `SHARD_ID`, `SHARD_TOTAL`, `MANIFEST_PATH`, `DATE_FOLDER`, and `OUT_DIR` from environment variables.
- Manifest-driven shard assignment must be deterministic (`hash(slug) % SHARD_TOTAL`) and only process assigned files; unassigned files must be skipped.
- Downloads must use HF CDN URLs without Authorization headers and must raise on non-2xx responses; timeouts must be configurable and default to 30s.
- Parquet reading must project heterogeneous rows to `{prompt, response}` and skip rows missing either field; malformed rows must be logged and skipped without crashing the worker.
- Deduplication must use `lib/dedup.py` and avoid emitting records with duplicate `_md5` within the same run; output must be written to `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` and the process exit code must be nonzero on fatal failure so GitHub Actions can retry.

## security — axentx-security @ 2026-05-03T01:59:34.961363Z

{"verdict": "OK", "findings": [{"severity": "low", "class": "other", "detail": "The code uses environment variables for configuration, which may lead to security issues if not properly validated and sanitized.", "mitigation": "Validate and sanitize environment variables to prevent potential security issues."}, {"severity": "med", "class": "other", "detail": "The code downloads files from a CDN without verifying the integrity of the downloads, which may lead to security issues if the downloads are tampered with.", "mitigation": "Implement download integrity verification, such as checksum validation, to ensure the downloads are authentic and untampered."}], "summary": "The proposed change introduces a Python worker that replaces a brittle shell script, but may have some security concerns related to environment variable validation and download integrity verification."}

## qa — security @ 2026-05-03T01:59:34.961390Z

{"verdict": "OK", "findings": [{"severity": "low", "class": "other", "detail": "The code uses environment variables for configuration, which may lead to security issues if not properly validated and sanitized.", "mitigation": "Validate and sanitize environment variables to prevent potential security issues."}, {"severity": "med", "class": "other", "detail": "The code downloads files from a CDN without verifying the integrity of the downloads, which may lead to security issues if the downloads are tampered with.", "mitigation": "Implement download integrity verification, such as checksum validation, to ensure the downloads are authentic and untampered."}], "summary": "The proposed change introduces a Python worker that replaces a brittle shell script, but may have some security concerns related to environment variable validation and download integrity verification."}
