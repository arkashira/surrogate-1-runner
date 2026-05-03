# axentx-dev-bot decision
- id: `20260503-004502-surrogate-1-discovery-597cf2af`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:45:02.274527Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:45:02.274585Z

## Final Implementation Plan (≤2h)

**Highest-value change**: Add `tools/snapshot_manifest.py` that lists one date-partition via a **single** HF API call, emits `file_manifest.json` with CDN URLs, and a training script that uses **CDN-only** fetches (zero HF API calls during training). This applies the CDN bypass pattern to avoid HF API rate limits while enabling Lightning Studio reuse.

### Steps (1h 45m total)

1. **Create tools/snapshot_manifest.py** (30m)  
   - Single `list_repo_tree` call for a date folder (e.g., `public-merged/2026-05-03`)  
   - Emit `file_manifest.json`: `{ "date": "...", "files": [ { "path": "...", "cdn_url": "...", "size": ... } ] }`  
   - Include repo, partition, and generation timestamp

2. **Create train_cdn.py** (45m)  
   - Load `file_manifest.json`  
   - Use `requests` to stream each CDN URL directly (no `datasets.load_dataset`)  
   - Parse each file to `{prompt, response}` only at parse time  
   - Yield examples for PyTorch DataLoader or HF Dataset from memory-mapped files  
   - Zero HF API calls during training loop  
   - Include retry logic (3 attempts with exponential backoff) for CDN resilience

3. **Create launcher notebook/script for Lightning Studio** (20m)  
   - Reuse running Studio if available (`Teamspace.studios` check)  
   - Upload `file_manifest.json` and `train_cdn.py` to Studio  
   - Start with `Machine.L40S` (or fallback to public tier)  
   - Handle idle-stop: check status before `.run()` and restart if stopped

4. **Update README** (10m)  
   - Add usage: `python tools/snapshot_manifest.py --date 2026-05-03 --repo axentx/surrogate-1-training-pairs`  
   - Document CDN-only training and Studio reuse

---

## tools/snapshot_manifest.py

```python
#!/usr/bin/env python3
"""
snapshot_manifest.py
List one date-partition of axentx/surrogate-1-training-pairs via a single
HF API call and emit file_manifest.json with CDN URLs.

Usage:
  python tools/snapshot_manifest.py --date 2026-05-03 --repo axentx/surrogate-1-training-pairs
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import huggingface_hub

HF_REPO = "axentx/surrogate-1-training-pairs"
CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def list_partition(repo: str, date: str) -> list[dict]:
    """
    Single API call: list top-level files under public-merged/<date>/
    """
    prefix = f"public-merged/{date}/"
    try:
        tree = huggingface_hub.list_repo_tree(
            repo=repo,
            path=prefix,
            recursive=False,
            repo_type="dataset",
        )
    except Exception as exc:
        print(f"ERROR listing repo tree for {prefix!r}: {exc}", file=sys.stderr)
        raise

    files = []
    for entry in tree:
        if entry.type != "file":
            continue
        path = entry.path
        files.append(
            {
                "path": path,
                "cdn_url": CDN_TEMPLATE.format(repo=repo, path=path),
                "size": getattr(entry, "size", None),
                "lfs": getattr(entry, "lfs", None),
            }
        )
    return files

def build_manifest(date: str, repo: str, output_path: Path) -> None:
    files = list_partition(repo=repo, date=date)
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo": repo,
        "date": date,
        "partition_prefix": f"public-merged/{date}/",
        "total_files": len(files),
        "files": files,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote manifest with {len(files)} files -> {output_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Snapshot HF partition manifest (CDN URLs).")
    parser.add_argument("--date", required=True, help="Date partition (YYYY-MM-DD)")
    parser.add_argument("--repo", default=HF_REPO

## review — reviewer @ 2026-05-03T00:45:12.727465Z

APPROVE: Single-API-call manifest + CDN-only training is a workable, incremental step that directly addresses HF rate-limit risk and enables Lightning Studio reuse; manifest shape and retry/backoff are specified and implementable.

Acceptance criteria (downstream tester can check):
- `tools/snapshot_manifest.py --date 2026-05-03 --repo axentx/surrogate-1-training-pairs` exits 0 and produces `file_manifest.json` containing `date`, `repo`, `generated_at_utc`, `partition_prefix`, `total_files`, and per-file `path`, `cdn_url`, `size`.
- Each `cdn_url` in the manifest is a valid HTTPS URL pointing to `https://huggingface.co/datasets/{repo}/resolve/main/{path}` and returns 200 for at least one sample file.
- `train_cdn.py --manifest file_manifest.json --batch-size N` loads the manifest, streams each CDN URL with retry (3 attempts, exponential backoff), parses `{prompt, response}` per example, and yields examples suitable for a PyTorch DataLoader or HF Dataset without any `datasets.load_dataset` or HF API calls during training.
- During a short training run (e.g., 2 batches), no HTTP request is made to `api-inference.huggingface.co` or `huggingface.co/api`; all fetches are to `huggingface.co/datasets/.../resolve/main/...`.
- Launcher notebook/script checks for an existing running Studio in `Teamspace.studios`, uploads `file_manifest.json` and `train_cdn.py`, starts on `Machine.L40S` (or public fallback), and handles idle-stop by checking status before `.run()` and restarting if stopped.

## qa — qa @ 2026-05-03T00:45:56.334177Z

PASS: criteria clear and implementable

1. **Acceptance criteria**
- `tools/snapshot_manifest.py --date 2026-05-03 --repo axentx/surrogate-1-training-pairs` exits 0 and produces `file_manifest.json` containing required keys: `date`, `repo`, `generated_at_utc`, `partition_prefix`, `total_files`, and per-file `path`, `cdn_url`, `size`.
- Every `cdn_url` is a valid HTTPS URL matching `https://huggingface.co/datasets/{repo}/resolve/main/{path}` and at least one sample file returns HTTP 200.
- `train_cdn.py --manifest file_manifest.json --batch-size N` loads manifest, streams each CDN URL with retry (3 attempts, exponential backoff), parses `{prompt, response}` per example, and yields examples suitable for PyTorch DataLoader or HF Dataset with zero `datasets.load_dataset` or HF API calls during training.
- During a short training run (e.g., 2 batches), no HTTP request is made to `api-inference.huggingface.co` or `huggingface.co/api`; all fetches are to `huggingface.co/datasets/.../resolve/main/...`.
- Launcher notebook/script checks for an existing running Studio in `Teamspace.studios`, uploads `file_manifest.json` and `train_cdn.py`, starts on `Machine.L40S` (or public fallback), and handles idle-stop by checking status before `.run()` and restarting if stopped.
- Manifest `generated_at_utc` is ISO-8601 UTC and within ±5 minutes of test execution time.
- Manifest `total_files` equals the number of file entries emitted and is ≥ 0.

2. **Unit tests**
```python
# tests/unit/test_snapshot_manifest.py
import json
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from tools.snapshot_manifest import list_partition, build_manifest, main

def test_list_partition_single_api_call():
    with patch("tools.snapshot_manifest.huggingface_hub.list_repo_tree") as mock_tree:
        mock_tree.return_value = [
            MagicMock(type="file", path="public-merged/2026-05-03/file1.jsonl", size=1024),
            MagicMock(type="file", path="public-merged/2026-05-03/file2.jsonl", size=2048),
            MagicMock(type="directory", path="public-merged/2026-05-03/subdir"),
        ]
        files = list_partition("owner/repo", "2026-05-03")
        assert len(files) == 2
        assert all("cdn_url" in f for f in files)
        mock_tree.assert_called_once()

def test_build_manifest_structure():
    files = [
        {"path": "public-merged/2026-05-03/file1.jsonl", "cdn_url": "https://huggingface.co/datasets/owner/repo/resolve/main/public-merged/2026-05-03/file1.jsonl", "size": 1024},
    ]
    manifest = build_manifest("owner/repo", "2026-05-03", files)
    assert manifest["date"] == "2026-05-03"
    assert manifest["repo"] == "owner/repo"
    assert "generated_at_utc" in manifest
    assert manifest["partition_prefix"] == "public-merged/2026-05-03"
    assert manifest["total_files"] == 1
    assert len(manifest["files"]) == 1

def test_cdn_url_format():
    from tools.snapshot_manifest import CDN_TEMPLATE
    repo = "axentx/surrogate-1-training-pairs"
    path = "public-merged/2026-05-03/file.jsonl"
    url = CDN_TEMPLATE.format(repo=repo, path=path)
    assert url.startswith("https://")
    assert "resolve/main" in url

def test_main_writes_valid_json(tmp_path):
    out = tmp_path / "file_manifest.json"
    with patch("tools.snapshot_manifest.huggingface_hub.list_repo_tree") as mock_tree, \
         patch("tools.snapshot_manifest.datetime") as mock_dt, \
         patch("sys.argv", ["snapshot_manifest.py", "--date", "2026-05-03", "--repo", "r", "--output", str(out)]):
        mock_tree.return_value = [MagicMock(type="file", path="public-merged/2026-05-03/f1.jsonl", size=100)]
        mock_dt.now.return_value = datetime(2026, 5, 3, 12, 0, 0, tzinfo=timezone.utc)
        main()
        data = json.loads(out.read_text())
        assert data["date"] == "2026-05-03"
        assert data["total_files"] == 1
```

```python
# tests/unit/test_train_cdn.py

