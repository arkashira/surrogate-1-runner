# axentx-dev-bot decision
- id: `20260502-223724-surrogate-1-backend-c9fdd471`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-02T22:37:24.500154Z

## dev — claude/llm-fallback-chain @ 2026-05-02T22:37:24.500213Z

Below is the single, merged implementation that keeps every concrete, high-leverage idea from both proposals and removes contradictions.  
The plan is ordered so you can execute it in ≤ 2 h and immediately stop HF API 429s during training.

---

## Final plan (≤2 h)

**Highest-value improvement**  
Add deterministic pre-flight file listing + CDN-only ingestion so shard workers and training jobs make **zero** `/api/` calls and avoid 429s and mixed-schema pyarrow errors.

1. `bin/list-files.py` – one-time script that calls `list_repo_tree` once per folder and writes `file-list.json` (path, size, sha256, cdn_url).  
2. `lib/cdn_stream.py` – robust CDN iterator that downloads via raw CDN URLs with retries/backoff and yields only `{prompt, response}` (no schema coercion).  
3. `bin/cdn-fetch.py` – standalone downloader used by `dataset-enrich.sh` for parquet→jsonl projection.  
4. Update `bin/dataset-enrich.sh` to accept `FILE_LIST` and use CDN-first workflow while preserving existing upload path.  
5. Add minimal `bin/train-cdn.py` snippet showing Lightning + CDN-only training.

---

## 1) `bin/list-files.py`

Deterministic, one-call-per-folder file listing.

```python
#!/usr/bin/env python3
"""
Usage:
  HF_TOKEN=... python bin/list-files.py \
    --repo axentx/surrogate-1-training-pairs \
    --out file-list.json \
    [--folder batches/public-merged/2026-05-02]

Writes:
{
  "repo": "...",
  "folder": "...",
  "generated_at_utc": "...",
  "files": [
    {"path": "...", "size": 123, "sha256": "...", "cdn_url": "..."},
    ...
  ],
  "count": N
}
"""

import argparse
import json
import os
import sys
from datetime import datetime

from huggingface_hub import HfApi, RepositoryTreeEntry

CDN_BASE = "https://huggingface.co/datasets"

def list_folder(api: HfApi, repo: str, folder: str) -> list[dict]:
    entries = api.list_repo_tree(repo=repo, path=folder.rstrip("/"), recursive=False)
    out = []
    for e in entries:
        if isinstance(e, RepositoryTreeEntry) and e.type == "file":
            out.append({
                "path": e.path,
                "size": e.size or 0,
                "lfs": getattr(e, "lfs", None) is not None,
                "sha256": getattr(e, "sha256", None),
                "cdn_url": f"{CDN_BASE}/{repo}/resolve/main/{e.path}"
            })
    out.sort(key=lambda x: x["path"])
    return out

def main() -> None:
    parser = argparse.ArgumentParser(description="List dataset files for CDN ingestion")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--out", default="file-list.json")
    parser.add_argument("--folder", default="batches/public-merged")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN env var required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)
    folder = args.folder.rstrip("/")

    try:
        files = list_folder(api, args.repo, folder)
    except Exception as exc:
        print(f"ERROR listing repo tree: {exc}", file=sys.stderr)
        sys.exit(1)

    payload = {
        "repo": args.repo,
        "folder": folder,
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "files": files,
        "count": len(files),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()
```

```bash
chmod +x bin/list-files.py
```

---

## 2) `lib/cdn_stream.py`

CDN-only iterator that yields `{prompt, response}` without schema coercion.

```python
"""
lib/cdn_stream.py

Usage:
  from lib.cdn_stream import iter_cdn_parquet
  for item in iter_cdn_parquet(file_list, max_retries=5):
      ...
"""

import json
import time
from pathlib import Path
from typing import Iterable, Dict, Any

import pyarrow.parquet as pq
import requests

CDN_TIMEOUT = 30

def _download(url: str, out_path: Path, max_retries: int = 

## review — reviewer @ 2026-05-02T22:38:49.826861Z

APPROVE: Proposes a concrete, incremental plan that directly targets 429s by moving to CDN-only ingestion and provides runnable code for deterministic file listing and CDN streaming; workable first step with clear acceptance criteria a tester can validate.

- `bin/list-files.py` runs end-to-end (with HF_TOKEN) and produces valid `file-list.json` containing repo, folder, generated_at_utc, and sorted file entries with path/size/sha256/cdn_url.  
- `lib/cdn_stream.py` (and any companion downloader) can be imported and iterates CDN-hosted parquet files without making `/api/` calls during training, yielding `{prompt, response}` rows and retrying transient failures.  
- `bin/dataset-enrich.sh` accepts a `FILE_LIST` argument and, when provided, uses the CDN-first workflow (download via CDN URLs) while preserving the existing upload path for backward compatibility.  
- A minimal `bin/train-cdn.py` (or equivalent snippet) demonstrates Lightning or simple PyTorch training using only CDN URLs and the file list, with no HF API calls during the training loop.  
- No new secrets or credentials are introduced; CDN URLs remain public and no auth tokens are embedded in training jobs.

## qa — qa @ 2026-05-02T22:39:04.404013Z

PASS: criteria clear and implementable

1. **Acceptance criteria**
- `bin/list-files.py` exits 0 with HF_TOKEN, produces valid `file-list.json` containing repo, folder, generated_at_utc, count, and sorted files each with path (string), size (int ≥0), sha256 (string|null), cdn_url (string starting with `https://huggingface.co/datasets/`).
- `lib/cdn_stream.py` iterates CDN-hosted parquet files without any HTTP request whose path contains `/api/`; yields dicts with keys `prompt` and `response` (both strings) for every row; retries transient HTTP failures (status 429/5xx or network errors) with exponential backoff up to 3 attempts.
- `bin/cdn-fetch.py` downloads a file from a CDN URL to local path, verifies size matches expected (when provided), and exits 0 on success; on transient failure it retries (same policy as above) and exits non-zero on permanent failure.
- `bin/dataset-enrich.sh` accepts `FILE_LIST` env/arg; when provided, uses only CDN URLs for downloads (no `/api/` calls) and still produces the same upload artifact as the legacy path; when absent, falls back to original behavior without error.
- `bin/train-cdn.py` trains for 1 step/epoch using only CDN URLs and `file-list.json`, with zero HF API calls during the training loop (verified by network monitor or mock), and logs a training loss.
- No new secrets/credentials introduced: CDN URLs remain public and no HF_TOKEN is required for CDN reads or training.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_list_files.py
def test_list_files_output_schema(tmp_path, monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "fake")
    out = tmp_path / "file-list.json"
    # mock HfApi.list_repo_tree to return deterministic entries
    run_script("bin/list-files.py", ["--repo", "x/y", "--out", str(out), "--folder", "batches"])
    data = json.loads(out.read_text())
    assert "repo" in data and "folder" in data
    assert "generated_at_utc" in data
    assert isinstance(data["files"], list) and data["count"] == len(data["files"])
    for f in data["files"]:
        assert isinstance(f["path"], str) and len(f["path"]) > 0
        assert isinstance(f["size"], int) and f["size"] >= 0
        assert f.get("sha256") is None or isinstance(f["sha256"], str)
        assert f["cdn_url"].startswith("https://huggingface.co/datasets/")
    assert all(data["files"][i]["path"] <= data["files"][i+1]["path"] for i in range(len(data["files"])-1))

# test_cdn_stream.py
def test_cdn_stream_no_api_calls(mock_responses):
    # mock parquet CDN URL returning valid arrow with prompt/response columns
    mock_responses.get("https://huggingface.co/datasets/repo/file.parquet", body=parquet_bytes())
    stream = cdn_stream(["https://huggingface.co/datasets/repo/file.parquet"])
    rows = list(stream)
    assert all("prompt" in r and "response" in r for r in rows)
    assert not any("/api/" in req.url for req in mock_responses.calls)

def test_cdn_stream_retries_transient(mock_responses):
    mock_responses.get("https://huggingface.co/datasets/repo/file.parquet", [
        {"status": 502}, {"status": 502}, {"body": parquet_bytes()}
    ])
    rows = list(cdn_stream(["https://huggingface.co/datasets/repo/file.parquet"], retries=3))
    assert len(rows) > 0
    assert len(mock_responses.calls) == 3

# test_cdn_fetch.py
def test_cdn_fetch_success(tmp_path, mock_responses):
    url = "https://huggingface.co/datasets/repo/file.txt"
    mock_responses.get(url, body="hello")
    out = tmp_path / "out.txt"
    rc = run_fetch(url, out, expected_size=5)
    assert rc == 0 and out.read_text() == "hello"

def test_cdn_fetch_size_mismatch(tmp_path, mock_responses):
    url = "https://huggingface.co/datasets/repo/file.txt"
    mock_responses.get(url, body="hello")
    out = tmp_path / "out.txt"
    rc = run_fetch(url, out, expected_size=99)
    assert rc != 0

# test_dataset_enrich.sh (bash unit via bats or sharness)
@test "dataset-enrich.sh with FILE_LIST uses CDN only" {
    export FILE_LIST=file-list.json
  
