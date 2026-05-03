# axentx-dev-bot decision
- id: `20260503-004516-surrogate-1-discovery-235adc3d`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:45:16.607088Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:45:16.607145Z

## Final Implementation Plan (≤2h)

**Highest-value change**: Add a Mac-side `tools/snapshot_manifest.py` that lists one date-partition via a **single** HF API call, emits `file_manifest.json` with CDN URLs, and a training script that uses **CDN-only** fetches (zero HF API calls during training). This implements the CDN bypass pattern and prevents 429 rate limits during Lightning training.

### Steps (1h 30m total)

1. **Create tools/snapshot_manifest.py** (20m)  
   - Single `list_repo_tree` call for `public-merged/<date>/` (non-recursive)  
   - Deterministic sort for reproducibility  
   - Build CDN URLs: `https://huggingface.co/datasets/{repo}/resolve/main/{path}`  
   - Output `file_manifest.json` with `{date, repo, files: [{path, cdn_url, size}], generated_at}`  
   - Accept CLI args: `--repo`, `--date`, `--out`

2. **Create training/data_loader_cdn.py** (30m)  
   - Read `file_manifest.json`  
   - Use `requests.get(cdn_url, stream=True)` with retry/backoff  
   - Parse parquet → project `{prompt, response}` only (tolerate `input/output/completion` variants)  
   - Yield dicts; optional local per-file cache

3. **Update training/train.py** (20m)  
   - Import CDN loader; replace `load_dataset` calls  
   - Add CLI flag `--manifest` to point to manifest  
   - Ensure zero `huggingface_hub` API usage during training loop

4. **Add requirements-dev.txt** (5m)  
   - Include `requests`, `tqdm`, `pyarrow`, `pandas`

5. **Smoke test on Mac** (15m)  
   - Run snapshot script → verify manifest  
   - Run loader on 1 file → verify projection  
   - Dry-run training step (no actual epochs)

---

## Code Snippets

### tools/snapshot_manifest.py
```python
#!/usr/bin/env python3
"""
Generate CDN-only file manifest for a date partition.
Usage:
    python snapshot_manifest.py \
        --repo axentx/surrogate-1-training-pairs \
        --date 2026-04-29 \
        --out file_manifest.json
"""
import argparse
import json
import sys
from datetime import datetime

from huggingface_hub import HfApi

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CDN manifest for a date partition")
    parser.add_argument("--repo", required=True, help="HF dataset repo (e.g. axentx/surrogate-1-training-pairs)")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", default="file_manifest.json", help="Output JSON path")
    args = parser.parse_args()

    api = HfApi()
    folder_path = f"batches/public-merged/{args.date}"
    try:
        tree = api.list_repo_tree(repo_id=args.repo, path=folder_path, recursive=False)
    except Exception as e:
        print(f"Error listing repo tree: {e}", file=sys.stderr)
        sys.exit(1)

    files = []
    for item in sorted(tree, key=lambda x: x.path):
        if item.type != "file":
            continue
        path = f"{folder_path}/{item.path.split('/')[-1]}"
        files.append({
            "path": path,
            "cdn_url": CDN_TEMPLATE.format(repo=args.repo, path=path),
            "size": getattr(item, "size", None),
        })

    manifest = {
        "repo": args.repo,
        "date": args.date,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": files,
    }

    with open(args.out, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()
```

### training/data_loader_cdn.py
```python
import json
import time
from pathlib import Path
from typing import Iterator, Dict, Any

import pandas as pd
import pyarrow.parquet as pq
import requests
from tqdm import tqdm

RETRY_BACKOFF = (1, 2, 4, 8)  # seconds

def _fetch_with_retry(url: str, max_retries: int = 4) -> bytes:
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            return resp.conten

## review — reviewer @ 2026-05-03T00:45:21.251022Z

APPROVE: Workable first-step that implements the CDN-bypass pattern and gives a downstream tester concrete acceptance criteria; incremental progress that avoids HF API calls during training and mitigates 429 risk.

Acceptance criteria (for tester):
- Run `python tools/snapshot_manifest.py --repo <repo> --date <YYYY-MM-DD> --out file_manifest.json` and verify `file_manifest.json` exists, is valid JSON, contains `repo`, `date`, `generated_at`, and a `files` list where each entry has `path`, `cdn_url`, and `size` (size may be null).
- CDN URLs in the manifest resolve to downloadable content (HTTP 200) and are Parquet files.
- `training/data_loader_cdn.py` can be imported and `cdn_parquet_iterator(manifest_path)` yields dicts with keys `prompt` and `response` for at least one row from a sample manifest.
- During iteration, no `huggingface_hub` API calls occur (can verify by disabling network to HF API domains or monitoring traffic).
- Training script accepts `--manifest file_manifest.json` and completes at least one dry-run training step (no epochs required) using the CDN loader without raising schema or network errors.

## qa — qa @ 2026-05-03T00:45:32.926691Z

PASS: Proceed with implementation and test plan.

1. **Acceptance criteria**
- Running `python tools/snapshot_manifest.py --repo <repo> --date <YYYY-MM-DD> --out file_manifest.json` produces a valid `file_manifest.json` that exists and parses as JSON.
- Manifest top-level keys include `repo`, `date`, `generated_at`, and `files`; `files` is a list where each entry contains `path` (string), `cdn_url` (string), and `size` (number or null).
- Every `cdn_url` in the manifest responds to an HTTP HEAD/GET with status 200 and `Content-Type` indicating a Parquet file (or at least non-error response with `.parquet` extension).
- `training/data_loader_cdn.py` exports `cdn_parquet_iterator(manifest_path)` that yields dicts; for at least one row, keys include `prompt` and `response` (string values).
- During iteration by `cdn_parquet_iterator`, zero HTTP requests are made to `huggingface.co/api/` or `huggingface.co/huggingface_hub` paths (verifiable via request monitoring or network block).
- `training/train.py` with `--manifest file_manifest.json` completes a dry-run training step (one batch/step) without schema or network errors and without importing/using `huggingface_hub` at runtime.

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_snapshot_manifest.py
import json
from unittest.mock import MagicMock, patch
from tools.snapshot_manifest import main, CDN_TEMPLATE, build_manifest

def test_build_manifest_structure():
    items = [
        MagicMock(type="file", path="batches/public-merged/2026-04-29/file1.parquet"),
        MagicMock(type="file", path="batches/public-merged/2026-04-29/file2.parquet"),
    ]
    for idx, it in enumerate(items):
        it.size = 1024 * (idx + 1)
    manifest = build_manifest(repo="axentx/surrogate-1-training-pairs", date="2026-04-29", tree=items)
    assert manifest["repo"] == "axentx/surrogate-1-training-pairs"
    assert manifest["date"] == "2026-04-29"
    assert "generated_at" in manifest
    assert len(manifest["files"]) == 2
    for f in manifest["files"]:
        assert "path" in f and isinstance(f["path"], str)
        assert "cdn_url" in f and f["cdn_url"].startswith("https://")
        assert "size" in f

def test_cdn_url_format():
    items = [MagicMock(type="file", path="batches/public-merged/2026-04-29/x.parquet")]
    items[0].size = 2048
    manifest = build_manifest(repo="a/b", date="2026-04-29", tree=items)
    expected = CDN_TEMPLATE.format(repo="a/b", path="batches/public-merged/2026-04-29/x.parquet")
    assert manifest["files"][0]["cdn_url"] == expected

def test_main_writes_valid_json(tmp_path, monkeypatch):
    out = tmp_path / "out.json"
    mock_tree = [
        MagicMock(type="file", path="batches/public-merged/2026-04-29/f.parquet"),
    ]
    mock_tree[0].size = 512
    with patch("tools.snapshot_manifest.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.return_value = mock_tree
        with patch("sys.argv", ["snapshot_manifest.py", "--repo", "a/b", "--date", "2026-04-29", "--out", str(out)]):
            main()
    data = json.loads(out.read_text())
    assert data["repo"] == "a/b"
    assert data["date"] == "2026-04-29"
    assert isinstance(data["files"], list)

# tests/unit/test_data_loader_cdn.py
import json
from unittest.mock import mock_open, patch, MagicMock
from training.data_loader_cdn import cdn_parquet_iterator

def test_cdn_parquet_iterator_yields_prompt_response(tmp_path):
    manifest = {
        "repo": "a/b",
        "date": "2026-04-29",
        "generated_at": "2026-04-29T00:00:00Z",
        "files": [
            {"path": "batches/public-merged/2026-04-29/sample.parquet", "cdn_url": "https://example.com/sample.parquet", "size": 1024}
        ]
    }
    m_path = tmp_path / "manifest.json"
    m_path.write_text(json.dumps(manifest))

    fake_df = [{"prompt": "hello", "response": "world", "extra": 1}]
    with patch
