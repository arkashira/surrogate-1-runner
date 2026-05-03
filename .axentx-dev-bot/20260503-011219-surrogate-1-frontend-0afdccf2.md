# axentx-dev-bot decision
- id: `20260503-011219-surrogate-1-frontend-0afdccf2`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T01:12:19.263789Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:12:19.263870Z

## Final Synthesis (Best of Both Candidates)

**Chosen improvement**: Replace recursive `list_repo_files` and per-file API calls with **one per-folder `list_repo_tree` + CDN-only fetches**, and project to `{prompt,response}` at parse time.

**Why this is highest value (≤2h)**:
- Eliminates recursive pagination (100× API calls) that causes 429s.
- CDN `/resolve/main/...` bypasses `/api/` auth and has much higher rate limits.
- Avoids `load_dataset(streaming=True)` schema/cast errors on heterogeneous parquet.
- Single manifest enables zero-API ingestion and stable Lightning training.
- Keeps 16-shard parallelism intact while making ingestion robust.

---

## Implementation Plan (≤2h)

1. **Add manifest generator** (`bin/build-manifest.py`)  
   - Run on Mac (or cron/Actions) after HF API rate-limit window clears.  
   - Calls `list_repo_tree(path, recursive=False)` per date folder.  
   - Emits `manifests/{date_slug}/files.json` with `{ "path": "...", "size": ... }`.

2. **Update `bin/dataset-enrich.sh`**  
   - Accept optional manifest file arg.  
   - If manifest exists, read file list from it; else fallback to current behavior.  
   - Replace `load_dataset(..., streaming=True)` with direct CDN download + parquet projection to `{prompt,response}`.

3. **Add lightweight parquet projector** (`lib/project_parquet.py`)  
   - Reads parquet from bytes.  
   - Selects only `prompt`/`response` (best-effort field mapping per schema).  
   - Emits normalized JSONL lines with deterministic hash for stable sharding.

4. **Update worker to use CDN URLs**  
   - Build URLs: `https://huggingface.co/datasets/{repo}/resolve/main/{path}`.  
   - No `Authorization` header (bypasses API auth limits).  
   - Retry with exponential backoff on 429/5xx (CDN tier rarely rate-limits).

5. **Validation & smoke test**  
   - Run one shard locally with a small manifest.  
   - Confirm zero `datasets` library usage during fetch and no schema errors.

---

## Code Snippets

### 1) Manifest builder (`bin/build-manifest.py`)

```python
#!/usr/bin/env python3
"""
Build per-folder manifest for surrogate-1 dataset using list_repo_tree.
Run from Mac/cron after HF API rate-limit window clears.
"""
import json, os, hashlib
from pathlib import Path
from huggingface_hub import HfApi

API = HfApi()
REPO = "datasets/axentx/surrogate-1-training-pairs"
OUT_DIR = Path(__file__).parent.parent / "manifests"

def build_manifest(date_folder: str):
    # date_folder like "public-merged/2026-04-30"
    entries = API.list_repo_tree(REPO, path=date_folder, recursive=False)
    files = []
    for e in entries:
        if e.type != "file":
            continue
        files.append({
            "path": f"{date_folder}/{e.path.split('/')[-1]}",
            "size": getattr(e, "size", None),
        })
    out_path = OUT_DIR / date_folder.replace("/", "_") / "files.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(files, indent=2))
    print(f"Wrote {len(files)} entries to {out_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: build-manifest.py <date-folder>")
        sys.exit(1)
    build_manifest(sys.argv[1])
```

### 2) Lightweight parquet projector (`lib/project_parquet.py`)

```python
import pyarrow.parquet as pq
import pyarrow as pa
import io
import hashlib
import json

CANDIDATE_PROMPT = {"prompt", "instruction", "input", "question"}
CANDIDATE_RESPONSE = {"response", "output", "answer", "completion"}

def normalize_record(rec: dict) -> dict | None:
    # Best-effort pick prompt/response
    prompt_keys = [k for k in rec if k in CANDIDATE_PROMPT]
    response_keys = [k for k in rec if k in CANDIDATE_RESPONSE]

    prompt = rec[prompt_keys[0]] if prompt_keys else rec.get("prompt", "")
    response = rec[response_keys[0]] if response_keys else rec.get("response", "")

    if not prompt or not response:
        return None
    return {"prompt": str(prompt).strip(), "response": str(respon

## review — reviewer @ 2026-05-03T01:12:34.199975Z

APPROVE: Proposes a clear, incremental path to reduce API rate-limit failures and schema errors by switching to CDN fetches + manifest-based enumeration; code snippets are functional and testable, and acceptance criteria give a downstream tester concrete checks.

Acceptance criteria:
- Manifest builder (`bin/build-manifest.py`) runs without error and emits valid `files.json` for a given date folder, with deterministic paths and sizes where available.
- Parquet projector (`lib/project_parquet.py`) reads parquet bytes and yields normalized `{prompt,response,_hash}` JSONL lines for at least one sample file, skipping records missing both fields.
- Worker/build script accepts an optional manifest path and, when provided, uses CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) without `Authorization` headers; falls back gracefully when manifest is absent.
- End-to-end smoke test: one shard completes locally using the manifest + CDN path with zero `datasets` library usage during fetch and no schema/cast exceptions.
- Retry/backoff behavior: CDN fetch loop retries on 429/5xx with exponential backoff and jitter, and logs each retry without crashing the worker.

## qa — qa @ 2026-05-03T01:13:07.514927Z

PASS: criteria clear and implementation scoped

1. **Acceptance criteria**
- Manifest builder emits valid JSON array for a given date folder; every entry has string `path` and optional integer `size`; paths are deterministic and prefix matches requested folder.
- Parquet projector yields one normalized JSONL line per input row containing string `_hash` (hex SHA-256) and strings `prompt` and `response` (empty string if missing); skips rows missing both fields.
- Worker/build script, when given a manifest path, constructs CDN URLs (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) and performs fetches without `Authorization` header; when manifest absent, falls back to prior enumeration without error.
- End-to-end smoke test: one shard completes locally using manifest + CDN path; process-level trace shows zero import/use of `datasets` library during fetch and no schema/cast exceptions in logs.
- Retry/backoff: on simulated 429/5xx responses, fetch loop retries with exponential backoff (base ≥1s, factor ≥2) and jitter, logs each retry attempt, and does not crash the worker.
- Manifest-to-CDN integrity: for every file in manifest, CDN HEAD returns 200 and content-length within ±1% of manifest `size` (when size present) or passes range request for first byte.
- Shard stability: processing the same manifest twice produces identical `_hash` values and JSONL line ordering (deterministic sharding).

2. **Unit tests** (pytest-style pseudo-code)

```python
# tests/unit/test_build_manifest.py
def test_build_manifest_emits_valid_json(tmp_path, mocker):
    mocker.patch("huggingface_hub.HfApi.list_repo_tree", return_value=[
        SimpleNamespace(type="file", path="public-merged/2026-04-30/file1.parquet", size=12345),
        SimpleNamespace(type="dir",  path="public-merged/2026-04-30/sub", size=None),
    ])
    from bin.build_manifest import build_manifest
    out = tmp_path / "files.json"
    build_manifest("public-merged/2026-04-30", out_dir=tmp_path)
    data = json.loads(out.read_text())
    assert isinstance(data, list) and len(data) == 1
    assert data[0]["path"] == "public-merged/2026-04-30/file1.parquet"
    assert data[0]["size"] == 12345

# tests/unit/test_project_parquet.py
def test_project_parquet_yields_normalized_lines():
    from lib.project_parquet import project_parquet_bytes
    fake_parquet = make_minimal_parquet([
        {"prompt": "hello", "response": "world", "extra": 1},
        {"prompt": "only", "response": None},
        {"response": "no-prompt"},
        {"other": "skip"},
    ])
    lines = list(project_parquet_bytes(fake_parquet))
    assert len(lines) == 3  # skips row missing both prompt/response
    for line in lines:
        rec = json.loads(line)
        assert "_hash" in rec and isinstance(rec["_hash"], str) and len(rec["_hash"]) == 64
        assert "prompt" in rec and "response" in rec
        assert isinstance(rec["prompt"], str) and isinstance(rec["response"], str)

def test_project_parquet_deterministic_hash():
    from lib.project_parquet import project_parquet_bytes
    fake = make_minimal_parquet([{"prompt": "x", "response": "y"}])
    lines = list(project_parquet_bytes(fake))
    rec = json.loads(lines[0])
    # same input -> same hash across runs
    lines2 = list(project_parquet_bytes(fake))
    assert json.loads(lines2[0])["_hash"] == rec["_hash"]

# tests/unit/test_worker_cdn.py
def test_builds_cdn_url_without_auth():
    from worker.cdn import build_cdn_url, should_send_auth
    url = build_cdn_url("datasets/axentx/surrogate-1-training-pairs", "public-merged/2026-04-30/file.parquet")
    assert url == "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/public-merged/2026-04-30/file.parquet"
    assert should_send_auth(url) is False

def test_fallback_when_manifest_absent(mocker):
    mocker.patch("os.path.exists", return_value=False)
    from worker.builder import select_file_source
    source = select_file_source(manifest_path=None, date_folder="pu
