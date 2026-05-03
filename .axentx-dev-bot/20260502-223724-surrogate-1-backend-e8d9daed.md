# axentx-dev-bot decision
- id: `20260502-223724-surrogate-1-backend-e8d9daed`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-02T22:37:24.193562Z

## dev — claude/llm-fallback-chain @ 2026-05-02T22:37:24.193816Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Add deterministic pre-flight file listing + CDN-only ingestion to eliminate HF API 429s during training and make shard workers resilient.

### What we’ll do
1. Add `bin/list-files.py` — one-time Mac/CI script that calls `list_repo_tree` once per date folder and writes `file-list.json` (path + size + sha256). Embed this list in training/shard scripts so workers do **zero API calls** during data load.
2. Update `bin/dataset-enrich.sh` to accept an optional `FILE_LIST_JSON` env var; when present, workers stream from CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) instead of using `load_dataset(...)`.
3. Add `lib/cdn_stream.py` — lightweight CDN fetcher with backoff, range checks, and line-by-line JSONL/parquet projection to `{prompt, response}` only.

### Why this matters
- Avoids `load_dataset(streaming=True)` on heterogeneous repos (prevents pyarrow CastError).
- Bypasses `/api/` auth checks → CDN limits are much higher; no 429s during heavy training.
- Keeps HF API usage to a single `list_repo_tree` call per folder (fits within 1000/5min).
- Shard workers remain independent; no shared state required.

---

## 1) `bin/list-files.py`

```python
#!/usr/bin/env python3
"""
Single HF API call to list files for a date folder.

Usage:
  HF_TOKEN=<token> python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json

Produces:
[
  {"path": "batches/public-merged/2026-05-02/shard0-120000.jsonl", "size": 12345, "sha256": "..."},
  ...
]
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token)

    folder = f"batches/public-merged/{args.date}"
    entries = api.list_repo_tree(repo_id=args.repo, path=folder, recursive=True)

    files = []
    for e in entries:
        if getattr(e, "type", None) != "file":
            continue
        path = getattr(e, "path", None)
        if not path:
            continue
        size = getattr(e, "size", None)
        sha256 = getattr(e, "lfs", {}).get("sha256", None) if getattr(e, "lfs", None) else None
        files.append({"path": path, "size": size or 0, "sha256": sha256})

    # Deterministic ordering for stable shard assignment
    files.sort(key=lambda x: x["path"])

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(files, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")


if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x bin/list-files.py
```

---

## 2) `lib/cdn_stream.py`

```python
import json
import pyarrow.parquet as pq
import pyarrow as pa
import requests
import time
import tempfile
import os
from typing import Iterator, Dict, Any, Optional


def cdn_download(repo: str, path: str, out_path: str, max_retries: int = 3) -> None:
    url = f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"
    for attempt in range(1, max_retries + 1):
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return
        except Exception as exc:
            if attempt == max_retries:
                raise
            sleep = 2 ** attempt
            time.sleep(sleep)


def project_to_prompt_response(path: str, tmp_path: str) -> Iterator[Dict[str, Any]]:
    """Yield {prompt, response} records from JSONL or Parquet."""
    try:
        if path.endswith(".parquet"):
            tbl = pq.read_table(tmp_pat

## review — reviewer @ 2026-05-02T22:38:49.146064Z

APPROVE — deterministic pre-flight listing + CDN-only ingestion is a clear, workable step toward eliminating HF API 429s and making shard workers resilient; the provided snippets are functional starting points a downstream tester can validate.

Acceptance criteria:
- `bin/list-files.py` runs end-to-end with a valid `HF_TOKEN` and produces deterministic `file-list.json` for a given date folder (paths sorted, size/sha256 captured).
- `lib/cdn_stream.py` can download a sample JSONL/Parquet file from CDN and yield `{prompt, response}` records without calling `load_dataset`.
- `bin/dataset-enrich.sh` accepts `FILE_LIST_JSON` and, when present, uses CDN URLs (or the new streamer) instead of `load_dataset` for worker ingestion.
- Shard assignment logic (hash-based modulo) is deterministic across workers and reproducible for the same `file_list`.
- Failures during CDN download or parsing are non-fatal for individual files (skip + stderr log) and do not halt the entire shard job.

## qa — qa @ 2026-05-02T22:39:03.326374Z

PASS: deterministic pre-flight listing + CDN-only ingestion plan is clear and testable.

1) **Acceptance criteria**
- `bin/list-files.py` exits 0 with valid HF_TOKEN and produces `file-list.json` containing only file-type entries for the requested date folder; output is valid JSON array sorted by path; each entry has path (string), size (non-negative int), sha256 (string or null).
- `lib/cdn_stream.py` yields `{prompt, response}` dicts from CDN JSONL/Parquet URLs without invoking `load_dataset`; yields only records containing both fields; skips malformed rows and logs warnings to stderr.
- `bin/dataset-enrich.sh` when `FILE_LIST_JSON` is set uses CDN URLs (or `cdn_stream`) for ingestion and does not call `load_dataset`; when unset, falls back to original behavior.
- Shard assignment is deterministic: for a fixed `file_list`, worker index `i` and total workers `N`, the same file is assigned to the same worker across runs (hash-based modulo on path).
- CDN/download failures or parse errors are non-fatal per file: individual file failures are logged to stderr and skipped, and the overall job continues; exit code is 0 if at least one file succeeds, non-zero only if zero files processed.

2) **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_list_files.py
import json, tempfile, os
from unittest.mock import MagicMock, patch
from bin.list_files import main as list_files_main

def test_list_files_produces_sorted_json():
    with patch("bin.list_files.HfApi") as MockApi, tempfile.NamedTemporaryFile(mode="w", delete=False) as out:
        mock_api = MagicMock()
        mock_api.list_repo_tree.return_value = [
            MagicMock(type="file", path="batches/public-merged/2026-05-02/b.jsonl", size=200, lfs={}),
            MagicMock(type="file", path="batches/public-merged/2026-05-02/a.jsonl", size=100, lfs={"sha256": "abc"}),
            MagicMock(type="dir", path="batches/public-merged/2026-05-02/sub", size=None, lfs=None),
        ]
        MockApi.return_value = mock_api
        os.environ["HF_TOKEN"] = "fake"
        sys.argv = ["list-files.py", "--repo", "owner/repo", "--date", "2026-05-02", "--out", out.name]
        list_files_main()
        with open(out.name) as f:
            data = json.load(f)
        assert len(data) == 2
        assert [x["path"] for x in data] == sorted([x["path"] for x in data])
        assert all("size" in x and isinstance(x["size"], int) and x["size"] >= 0 for x in data)
        assert all("sha256" in x for x in data)

# tests/unit/test_cdn_stream.py
import io, pyarrow as pa, pyarrow.parquet as pq
from unittest.mock import patch, MagicMock
from lib.cdn_stream import cdn_lines, cdn_parquet_projection

def test_cdn_lines_yields_prompt_response():
    content = b'{"prompt":"p1","response":"r1"}\n{"prompt":"p2"}\ninvalid\n{"prompt":"p3","response":"r3"}'
    with patch("lib.cdn_stream.requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.iter_lines.return_value = iter(content.split(b"\n"))
        mock_get.return_value = mock_resp
        records = list(cdn_lines("https://cdn.example/file.jsonl"))
        assert len(records) == 2
        assert all("prompt" in r and "response" in r for r in records)

def test_cdn_parquet_projection_yields_prompt_response():
    table = pa.table({"prompt": ["p1", "p2"], "response": ["r1", "r2"], "extra": [1, 2]})
    buf = io.BytesIO()
    pq.write_table(table, buf)
    buf.seek(0)
    with patch("lib.cdn_stream.requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.content = buf.getvalue()
        mock_get.return_value = mock_resp
        records = list(cdn_parquet_projection("https://cdn.example/file.parquet"))
        assert len(records) == 2
        assert all("prompt" in r and "response" in r for r in records)
        assert all("extra" not in r for r in records)

# tests/unit/test_shard_assign.py
from lib.shard_assign import assign_shard

def test_shard_assignment_deterministic():
    files = [{"path": 
