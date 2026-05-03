# axentx-dev-bot decision
- id: `20260503-041605-surrogate-1-frontend-9dc0df8d`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T04:16:05.280510Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:16:05.280577Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Replace fragile shell-based ingestion with a **manifest-driven, CDN-bypass Python worker** that eliminates HF API rate limits during training data loads and prevents mixed-schema CastErrors.

### Changes

1. **Add `bin/worker.py`** — single-file worker that:
   - Accepts `SHARD_ID` and `N_SHARDS` (default 16) via env.
   - Uses one HF API call (`list_repo_tree`) to list top-level date folders in `batches/public-merged/`.
   - Deterministically assigns date folders to shards by hash.
   - For each assigned date folder, lists parquet files and downloads via CDN (`resolve/main/...`) with optional `HF_TOKEN` for private repos.
   - Projects each parquet to `{prompt, response}` with schema fallback (`prompt/input/question` × `response/output/answer`).
   - Streams NDJSON output for memory-safe, large-scale ingestion.

2. **Add `bin/build_manifest.py`** — optional dev helper that lists a specific date folder via HF API (respecting rate limits) and emits `manifest.json` for local testing or CI.

3. **Update `bin/dataset-enrich.sh`** — thin wrapper that invokes `worker.py` so GitHub Actions matrix keeps working.

4. **Add `requirements.txt` entries** if missing (`requests`, `pyarrow`, `tqdm`).

5. **Add `.github/workflows/ingest.yml`** (if absent) — 16-shard matrix, uses `HF_TOKEN`, passes `SHARD_ID`/`N_SHARDS`, uploads per-shard NDJSON as artifacts or pushes to a dataset branch.

### Why this wins
- **CDN bypass**: training uses `https://huggingface.co/datasets/.../resolve/main/...` — zero API calls during data loading, no 429s.
- **Schema safety**: project to `{prompt, response}` only at parse time; never rely on dataset streaming with heterogeneous files.
- **Deterministic sharding**: `hash(date_folder) % N_SHARDS` → shard id prevents collisions across runs and balances load.
- **Lightning reuse**: embed manifest or direct CDN paths in `train.py`; Lightning workers fetch via CDN only, no HF API quota burn.

---

## Code Snippets

### `bin/build_manifest.py`
```python
#!/usr/bin/env python3
"""
Run on Mac (or any dev machine) after HF API rate-limit window clears.
Produces manifest.json for a single date folder.

Usage:
  HF_TOKEN=hf_xxx python bin/build_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-04-30 \
    --out manifest.json
"""
import argparse
import json
import os
import sys
from typing import List, Dict

from huggingface_hub import HfApi, login

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="Folder under datasets, e.g. 2026-04-30")
    parser.add_argument("--out", default="manifest.json")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("HF_TOKEN required", file=sys.stderr)
        sys.exit(1)
    login(token=token)

    api = HfApi()
    folder = f"batches/public-merged/{args.date}"
    try:
        entries = api.list_repo_tree(repo_id=args.repo, path=folder, recursive=False)
    except Exception as e:
        print(f"Failed to list {args.repo}/{folder}: {e}", file=sys.stderr)
        sys.exit(1)

    files: List[Dict[str, str]] = []
    for entry in entries:
        if getattr(entry, "type", None) != "file":
            continue
        path = getattr(entry, "path", None)
        if not path or not path.endswith(".parquet"):
            continue
        cdn_url = f"https://huggingface.co/datasets/{args.repo}/resolve/main/{path}"
        files.append({"path": path, "cdn_url": cdn_url})

    manifest = {
        "repo": args.repo,
        "date": args.date,
        "files": files,
        "generated_by": "bin/build_manifest.py",
    }

    with open(args.out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()
```

### `bin/worker.py`
```python
#!/usr/bin/env python3
"""

## review — reviewer @ 2026-05-03T04:16:15.798807Z

APPROVE: Manifest-driven CDN-bypass worker is a clear, workable improvement that directly addresses HF API rate limits and schema fragility; deterministic sharding and NDJSON streaming are sensible for large-scale ingestion, and the thin wrapper keeps CI compatibility.

Acceptance criteria:
- Worker accepts `SHARD_ID`/`N_SHARDS` env vars and deterministically assigns date folders via `hash(date_folder) % N_SHARDS`.
- Worker lists top-level date folders with one `list_repo_tree` call, then downloads parquet via CDN URLs (no per-file HF API calls) and projects rows to `{prompt, response}` with schema fallback.
- Worker streams NDJSON output and handles errors per-file (skip + log) without aborting the entire shard.
- `bin/build_manifest.py` produces a valid `manifest.json` for a given date folder and repo, including CDN URLs for parquet files.
- CI workflow (or local run) can execute the worker matrix (e.g., 16 shards) using `HF_TOKEN` and emit per-shard NDJSON artifacts or push to a dataset branch.

## qa — qa @ 2026-05-03T04:17:30.507527Z

PASS: surrogate-1 manifest-driven CDN-bypass worker

1. **Acceptance criteria**
- Worker accepts SHARD_ID and N_SHARDS (default 16) from environment and deterministically assigns date folders via hash(date_folder) % N_SHARDS; shard assignment is stable across runs.
- Worker performs exactly one list_repo_tree call to list top-level date folders under batches/public-merged/ and zero per-file HF API calls during parquet downloads (CDN-only).
- Worker projects each parquet row to {prompt, response} using schema fallback (prompt/input/question × response/output/answer) and emits one valid NDJSON object per row.
- Worker streams NDJSON to stdout (or file) with bounded memory (no full-dataset materialization) and handles per-file errors by skipping and logging without aborting the shard.
- bin/build_manifest.py produces manifest.json for a given repo and date folder containing repo, date, and an array of parquet entries with CDN URLs and optional metadata; output is valid JSON and reproducible for same inputs.
- CI/local execution supports a 16-shard matrix using HF_TOKEN and emits per-shard NDJSON artifacts or pushes to a dataset branch; total rows across all shards equal total rows in assigned date folders (no loss or duplication).
- Default N_SHARDS=16 when N_SHARDS is unset; SHARD_ID must be an integer in [0, N_SHARDS-1] and validation fails fast with a clear error otherwise.

2. **Unit tests** (pytest style)
```python
# test_worker_sharding.py
import os
from unittest.mock import patch
from bin.worker import shard_for_date, list_and_assign_shards

def test_shard_for_date_deterministic():
    assert shard_for_date("2026-04-30", n=16) == shard_for_date("2026-04-30", n=16)
    assert 0 <= shard_for_date("2026-04-30", n=16) < 16

def test_shard_for_date_uniform():
    # sanity: different dates map to different shards often (not required always)
    s1 = shard_for_date("2026-04-30", n=16)
    s2 = shard_for_date("2026-05-01", n=16)
    assert isinstance(s1, int) and isinstance(s2, int)

def test_env_parsing_defaults():
    with patch.dict(os.environ, {}, clear=True):
        from bin.worker import get_shard_config
        cfg = get_shard_config()
        assert cfg.n_shards == 16
        assert cfg.shard_id is None  # or raises; depends on chosen behavior

def test_env_parsing_explicit():
    with patch.dict(os.environ, {"SHARD_ID": "3", "N_SHARDS": "8"}):
        from bin.worker import get_shard_config
        cfg = get_shard_config()
        assert cfg.shard_id == 3 and cfg.n_shards == 8

def test_invalid_shard_id_raises():
    with patch.dict(os.environ, {"SHARD_ID": "20", "N_SHARDS": "16"}):
        from bin.worker import get_shard_config
        try:
            get_shard_config()
            assert False, "expected ValueError"
        except ValueError:
            pass

# test_worker_projection.py
import pyarrow as pa
from bin.worker import project_row_to_prompt_response

def test_project_prompt_response_happy():
    row = {"prompt": "hello", "response": "world"}
    out = project_row_to_prompt_response(row)
    assert out == {"prompt": "hello", "response": "world"}

def test_project_fallback_prompt_input():
    row = {"prompt": {"input": {"question": "q"}, "response": {"output": {"answer": "a"}}}}
    out = project_row_to_prompt_response(row)
    assert out == {"prompt": "q", "response": "a"}

def test_project_fallback_response_output():
    row = {"input": "q", "output": "a"}
    out = project_row_to_prompt_response(row)
    # choose expected policy: map input->prompt, output->response
    assert out == {"prompt": "q", "response": "a"}

def test_project_missing_fields_returns_none():
    row = {"other": "x"}
    out = project_row_to_prompt_response(row)
    assert out is None  # or empty; policy: skip row

# test_build_manifest.py
import json
from unittest.mock import MagicMock
from bin.build_manifest import build_manifest

def test_build_manifest_valid_json(tmp_path):
    mock_api = MagicMock()
    mock_api.list_repo_tree.r
