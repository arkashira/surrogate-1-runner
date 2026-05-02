# axentx-dev-bot decision
- id: `20260502-185802-surrogate-1-discovery-e1bcd027`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T18:58:02.469954Z

## dev — claude/llm-fallback-chain @ 2026-05-02T18:58:02.470042Z

## Highest-value incremental improvement (≤2h)

**Deterministic date-partitioned ingestion with CDN-bypass and pre-flight file-list**

- Fixes: non-deterministic overwrite/no-date-partition, redundant API calls, HF API rate-limits during ingestion.
- Outcome: stable `batches/public-merged/YYYY/MM/DD/shard-N-<ts>.jsonl`, single Mac-side file-list generation, workers fetch via CDN (zero auth/rate-limit), idempotent daily runs.

---

## Implementation plan

1. Add `bin/list-public-files.py` (run on Mac/CI before matrix)
   - Uses HF API **once** to list top-level date folders (or all files) for the public dataset.
   - Persists `file-list.json` (repo-root relative paths) + `run-manifest.json` (date, shard map, timestamp).
   - Commits or uploads as workflow artifact for the matrix.

2. Update `bin/dataset-enrich.sh`
   - Accept `FILE_LIST` (path to per-shard file list) and `DATE_ROOT` (e.g., `2026/05/02`).
   - Use `hf_hub_download`/`wget` against CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) — no Authorization header, bypasses `/api/` rate limits.
   - Output to `batches/public-merged/${DATE_ROOT}/shard${SHARD_ID}-${TS}.jsonl`.

3. Update `.github/workflows/ingest.yml`
   - Add job `prepare` that runs `python bin/list-public-files.py`, produces `file-list.json`, and splits into 16 shards (`shard-00.list`..`shard-15.list`) as artifacts.
   - Matrix job uses `needs.prepare`, downloads per-shard list + manifest, sets `DATE_ROOT` from manifest.
   - Keep 16 parallel runners; each worker only processes its shard list.

4. Small library helpers
   - Add `lib/cdn.py` with `cdn_url(repo, path)` and robust download (retry/backoff).
   - Keep `lib/dedup.py` unchanged (central dedup store remains source of truth).

5. Validation & rollback
   - Dry-run locally with a single shard to confirm CDN fetch and output path.
   - If CDN fails, fallback to authenticated `hf_hub_download` (logged).

---

## Code snippets

### bin/list-public-files.py
```python
#!/usr/bin/env python3
"""
Generate file-list and manifest for surrogate-1 public ingestion.
Run once per cron trigger (Mac/CI) before matrix workers start.
"""
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

REPO = "axentx/surrogate-1-training-pairs"
OUT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../artifacts"
os.makedirs(OUT_DIR, exist_ok=True)

def main() -> None:
    api = HfApi()
    # List top-level date folders (non-recursive) to avoid 429 on huge trees.
    items = api.list_repo_tree(repo_id=REPO, path="", recursive=False)
    date_folders = [
        it.rstrip("/") for it in items if it and not it.startswith(".") and "/" not in it.rstrip("/")
    ]

    # If repo uses flat file layout, fallback to listing known extensions.
    if not date_folders:
        # Conservative: list only first-level parquet/jsonl to reduce API pressure.
        items = api.list_repo_tree(repo_id=REPO, path="", recursive=False)
        files = [it for it in items if it and it.endswith((".parquet", ".jsonl", ".json"))]
        # Assign to today's partition for ingestion.
        date_root = datetime.now(timezone.utc).strftime("%Y/%m/%d")
        file_paths = files
    else:
        # Pick latest date folder (YYYY-MM-DD or YYYY/MM/DD style).
        date_folders.sort(reverse=True)
        latest = date_folders[0]
        # Normalize to YYYY/MM/DD
        if "-" in latest:
            parts = latest.split("-")
            if len(parts) == 3:
                date_root = f"{parts[0]}/{parts[1]}/{parts[2]}"
            else:
                date_root = latest.replace("-", "/")
        else:
            date_root = latest.replace("-", "/")

        # List files inside that date folder (non-recursive).
        sub_items = api.list_repo_tree(repo_id=REPO, path=latest, recursive=False)
        file_paths = [f"{latest}/{it}" for it in sub_items if it and it.endswith((".parquet", ".jsonl", ".json"))]

    manifest = {
        "repo

## review — reviewer @ 2026-05-02T18:58:21.054270Z

APPROVE: Deterministic, incremental progress that fixes non-deterministic overwrite and HF API pressure while remaining practical and testable.

Acceptance criteria (downstream tester can check):
- `python bin/list-public-files.py` produces `artifacts/run-manifest.json` and `artifacts/file-list.json` and 16 shard files (`shard-00.list`..`shard-15.list`) without error on a local checkout.
- Manifest contains `date_root`, `repo`, `created_utc`, `total_files`, and `files`; `date_root` matches `YYYY/MM/DD` pattern.
- A single shard worker can run the updated `dataset-enrich.sh` with `FILE_LIST` and `DATE_ROOT` and produce `batches/public-merged/${DATE_ROOT}/shardN-<ts>.jsonl` using CDN URLs (no Authorization header) and fall back to authenticated `hf_hub_download` on CDN failure (logged).
- CDN fetch succeeds for at least one known file in the repo (e.g., a small `.jsonl` or `.parquet`) and output file is valid JSONL lines (or parquet readable) and contains expected records.
- Matrix workflow in `.github/workflows/ingest.yml` can run the `prepare` job, upload shard artifacts, and the matrix job can consume them with `needs.prepare` and set `DATE_ROOT` from the manifest.

## qa — qa @ 2026-05-02T18:58:37.179523Z

PASS: Ready to implement deterministic date-partitioned ingestion.

1. **Acceptance criteria**
- `python bin/list-public-files.py` exits 0 and produces `artifacts/run-manifest.json`, `artifacts/file-list.json`, and 16 shard files (`shard-00.list`..`shard-15.list`) in ≤30s on a local checkout.
- `run-manifest.json` contains keys `date_root`, `repo`, `created_utc`, `total_files`, `files`; `date_root` matches `^\d{4}/\d{2}/\d{2}$` and `created_utc` is ISO-8601 with timezone.
- Running `dataset-enrich.sh` with `FILE_LIST` and `DATE_ROOT` produces `batches/public-merged/${DATE_ROOT}/shardN-<ts>.jsonl` where `<ts>` is a numeric timestamp; the worker uses CDN URLs without an Authorization header and logs fallback to authenticated `hf_hub_download` on CDN failure.
- For at least one known file in the repo, CDN fetch succeeds and output file is valid JSONL (each line is valid JSON) or valid Parquet (readable by pyarrow) and contains ≥1 record.
- Matrix workflow `ingest.yml` can execute the `prepare` job, upload shard artifacts, and the matrix job can consume them via `needs.prepare` and set `DATE_ROOT` from the manifest (dry-run via `act` or workflow syntax check passes).

2. **Unit tests**
```python
# tests/unit/test_list_public_files.py
import json, os, tempfile, pytest
from unittest.mock import MagicMock, patch
from bin.list_public_files import main as list_files_main

def test_produces_required_files():
    with tempfile.TemporaryDirectory() as td:
        artifacts = os.path.join(td, "artifacts")
        with patch("bin.list_public_files.HfApi") as MockApi, \
             patch("bin.list_public_files.os.makedirs"), \
             patch("bin.list_public_files.os.path.abspath", return_value=os.path.join(td, "bin")), \
             patch("sys.argv", ["list-public-files.py"]):
            mock_api = MagicMock()
            mock_api.list_repo_tree.return_value = ["2026/05/02/", "2026/05/03/"]
            MockApi.return_value = mock_api
            os.environ["OUT_DIR"] = artifacts
            list_files_main()
        assert os.path.exists(os.path.join(artifacts, "run-manifest.json"))
        assert os.path.exists(os.path.join(artifacts, "file-list.json"))
        for i in range(16):
            assert os.path.exists(os.path.join(artifacts, f"shard-{i:02d}.list"))

def test_manifest_schema_and_date_root_pattern():
    import re
    manifest_path = "artifacts/run-manifest.json"
    # assume file exists from previous test setup
    # in real test, create fixture
    with open(manifest_path) as f:
        m = json.load(f)
    assert re.match(r"^\d{4}/\d{2}/\d{2}$", m["date_root"])
    for k in ("repo", "created_utc", "total_files", "files"):
        assert k in m
    assert isinstance(m["total_files"], int) and m["total_files"] >= 0
    assert isinstance(m["files"], list)

# tests/unit/test_cdn.py
from lib.cdn import cdn_url, download_cdn
import re

def test_cdn_url():
    assert cdn_url("owner/repo", "2026/05/02/file.jsonl") == \
           "https://huggingface.co/datasets/owner/repo/resolve/main/2026/05/02/file.jsonl"

def test_download_cdn_fallback_logs(monkeypatch, caplog):
    import requests
    mock_get = MagicMock(side_effect=requests.exceptions.RequestError("CDN fail"))
    monkeypatch.setattr(requests, "get", mock_get)
    # fallback path should be attempted and logged
    with pytest.raises(Exception):
        download_cdn("owner/repo", "2026/05/02/file.jsonl", "/tmp/out")
    assert any("CDN" in r.message for r in caplog.records)
```

```python
# tests/unit/test_dataset_enrich_sh.py (shell behavior via subprocess)
import subprocess, os, tempfile, json, pytest

def test_dataset_enrich_sh_creates_output():
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "batches", "public-merged", "2026/05/02"), exist_ok=True)
        flist = os.path.join(td, "shard.list")
        with open(flist, "w") as f:
            f.write("2026/05/02/sample.jsonl\n")
        # mock CDN fetch by creating a dummy file in re
