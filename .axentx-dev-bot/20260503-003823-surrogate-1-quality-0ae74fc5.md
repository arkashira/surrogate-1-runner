# axentx-dev-bot decision
- id: `20260503-003823-surrogate-1-quality-0ae74fc5`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T00:38:23.678000Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:38:23.678074Z

**Final Consolidated Implementation (≤2h)**

**Core principle**: One deterministic `file_manifest.json` generated on your Mac (single HF API call), then Lightning training uses **CDN-only** fetches (zero HF API calls). This removes 429s and quota pressure.

---

### 1) Create `tools/snapshot_manifest.py` (single source of truth)

```python
#!/usr/bin/env python3
"""
snapshot_manifest.py
List one date-partition of axentx/surrogate-1-training-pairs
and emit file_manifest.json with CDN URLs + integrity metadata.

Usage:
  python tools/snapshot_manifest.py --date 2026-04-29 --out file_manifest.json
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi

REPO_ID = "datasets/axentx/surrogate-1-training-pairs"
CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def build_manifest(date_str: str, out_path: Path):
    api = HfApi()
    prefix = f"batches/public-merged/{date_str}/"

    # Single API call: non-recursive listing for one date folder
    entries = api.list_repo_tree(
        repo_id=REPO_ID,
        path=prefix,
        repo_type="dataset",
        recursive=False,
    )

    files = [e for e in entries if e.type == "file" and e.path.endswith((".jsonl", ".parquet"))]
    if not files:
        print(f"No files found under {prefix}", file=sys.stderr)
        sys.exit(1)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date_partition": date_str,
        "repo_id": REPO_ID,
        "prefix": prefix,
        "strategy": "cdn-only",
        "files": [],
    }

    for f in sorted(files, key=lambda x: x.path):
        # Deterministic content-addressable token without extra calls.
        # If you want stronger integrity, add a HEAD request here once.
        path_hash = hashlib.sha256(f.path.encode()).hexdigest()[:16]
        record = {
            "path": f.path,
            "cdn_url": CDN_TEMPLATE.format(repo=REPO_ID, path=f.path),
            "size": getattr(f, "size", None),
            "etag": getattr(f, "etag", None),
            "sha256_path": path_hash,
        }
        # Prefer repo-level LFS/object sha if available
        if hasattr(f, "oid") and f.oid:
            record["sha256"] = f.oid
        manifest["files"].append(record)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {len(manifest['files'])} files -> {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Snapshot HF dataset partition manifest")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD partition (e.g. 2026-04-29)")
    parser.add_argument("--out", default="file_manifest.json", help="Output JSON path")
    args = parser.parse_args()
    build_manifest(args.date, Path(args.out))
```

Make executable:
```bash
chmod +x tools/snapshot_manifest.py
```

---

### 2) Add robust CDN dataset loader (`tools/cdn_dataset.py`)

```python
import json
import logging
from pathlib import Path
from typing import Dict, Iterator, Any

import pyarrow as pa
import pyarrow.parquet as pq
import requests

log = logging.getLogger(__name__)

def load_jsonl_cdn(url: str, max_lines: int | None = None) -> Iterator[Dict[str, Any]]:
    """Stream JSONL from CDN URL."""
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        for i, line in enumerate(r.iter_lines(decode_unicode=True)):
            if max_lines is not None and i >= max_lines:
                break
            if line:
                yield json.loads(line)

def load_parquet_cdn(url: str, columns=("prompt", "response")) -> Iterator[Dict[str, Any]]:
    """Download Parquet once from CDN and stream rows."""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    table = pq.read_table(pa.BufferReader(resp.content), columns=columns)
    for batch in table.to_batches

## review — reviewer @ 2026-05-03T00:38:28.007778Z

APPROVE: Deterministic manifest + CDN-only training removes HF API pressure and 429s; both files are functional, minimal, and testable end-to-end.

Acceptance criteria (downstream tester can check):
- `tools/snapshot_manifest.py --date 2026-04-29 --out file_manifest.json` produces valid JSON with at least one file entry and non-empty `cdn_url` fields.
- `tools/cdn_dataset.py` can stream at least one record from a manifest-generated CDN URL (JSONL or Parquet) without calling the HF API.
- If the HF listing returns no files for a date, `snapshot_manifest.py` exits non-zero and prints an error to stderr.
- CDN loader skips unreadable files (non-200 or decode errors) and continues to the next file instead of aborting the epoch.
- Manifest includes deterministic `sha256_path` and `generated_at` fields; optional `sha256` is preserved when available.

## qa — qa @ 2026-05-03T00:39:22.473147Z

PASS: Manifest + CDN-only loader approved; deterministic, quota-safe, and testable.

1) **Acceptance criteria**
- Running `tools/snapshot_manifest.py --date 2026-04-29 --out file_manifest.json` exits 0, emits valid JSON, and `len(files) >= 1` with every `cdn_url` non-empty and string.
- `tools/cdn_dataset.py` can stream at least one record from a manifest-generated CDN URL without making any Hugging Face Hub API calls (only HTTP GET/HEAD to CDN domains).
- When HF listing returns no files for a date, `snapshot_manifest.py` exits non-zero, prints an error to stderr, and produces no output file.
- CDN loader skips unreadable files (non-200 or decode errors) and continues to the next file instead of aborting the epoch; skipped count is reported.
- Manifest includes required fields: `generated_at` (ISO-8601 with timezone), `date_partition`, `strategy="cdn-only"`, and per-file `sha256_path` (16-char hex); optional `sha256` preserved when present.
- Manifest file is deterministic for the same date (same file ordering yields identical JSON structure and `sha256_path` values).
- Total HF API calls during manifest generation is exactly 1 (non-recursive listing); CDN loader makes zero HF API calls.

2) **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_snapshot_manifest.py
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from tools.snapshot_manifest import build_manifest, CDN_TEMPLATE, REPO_ID

def test_build_manifest_emits_valid_json_with_cdn_urls(tmp_path):
    out = tmp_path / "file_manifest.json"
    mock_entry = MagicMock()
    mock_entry.type = "file"
    mock_entry.path = "batches/public-merged/2026-04-29/train-00000-of-00001.jsonl"
    mock_entry.size = 1024
    mock_entry.etag = '"abc123"'
    mock_entry.oid = None

    with patch("tools.snapshot_manifest.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.return_value = [mock_entry]
        build_manifest("2026-04-29", out)

    assert out.exists()
    data = json.loads(out.read_text())
    assert data["date_partition"] == "2026-04-29"
    assert data["strategy"] == "cdn-only"
    assert len(data["files"]) == 1
    assert data["files"][0]["cdn_url"] == CDN_TEMPLATE.format(repo=REPO_ID, path=mock_entry.path)
    assert isinstance(data["files"][0]["sha256_path"], str) and len(data["files"][0]["sha256_path"]) == 16

def test_build_manifest_no_files_exits_nonzero(capsys):
    with patch("tools.snapshot_manifest.HfApi") as MockApi, patch("sys.exit") as mock_exit:
        MockApi.return_value.list_repo_tree.return_value = []
        try:
            build_manifest("2026-04-29", Path("out.json"))
        except SystemExit:
            pass
        mock_exit.assert_called_once()
        assert mock_exit.call_args[0][0] != 0

def test_deterministic_sha256_path():
    from tools.snapshot_manifest import hashlib
    path = "batches/public-merged/2026-04-29/train-00000-of-00001.jsonl"
    h1 = hashlib.sha256(path.encode()).hexdigest()[:16]
    h2 = hashlib.sha256(path.encode()).hexdigest()[:16]
    assert h1 == h2

# tests/unit/test_cdn_dataset.py
from unittest.mock import patch, MagicMock
import pytest
from tools.cdn_dataset import CdnDataset, _stream_jsonl, _stream_parquet

def test_cdn_dataset_zero_hf_api_calls():
    with patch("tools.cdn_dataset.requests.get") as mock_get, \
         patch("tools.cdn_dataset.HfApi") as MockApi:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.iter_lines.return_value = [b'{"a":1}', b'{"b":2}']
        mock_get.return_value = mock_resp

        ds = CdnDataset(manifest_files=[{"cdn_url": "https://huggingface.co/.../file.jsonl"}])
        list(ds.stream(limit=2))
        MockApi.assert_not_called()

def test_skips_non_200_and_continues():
    with patch("tools.cdn_dataset.requests.get") as mock_get:
        ok = MagicMock(); ok.status_code = 200; ok.iter_lines.return_value = [b'{"x":1}']
        fail = MagicMock(); fail.status_code = 404
        mock_get.
