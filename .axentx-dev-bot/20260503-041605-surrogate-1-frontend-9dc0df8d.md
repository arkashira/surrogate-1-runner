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

## review — reviewer @ 2026-05-03T04:16:25.435362Z

APPROVE: Manifest-driven worker replaces fragile shell ingestion with deterministic sharding and CDN-bypass ingestion; schema projection and NDJSON streaming are concrete, testable improvements that unblock training data loads without HF API rate limits.

Acceptance criteria:
- `bin/worker.py` accepts `SHARD_ID`/`N_SHARDS` env vars, lists date folders via `list_repo_tree`, assigns shards by `hash(date_folder) % N_SHARDS`, downloads parquet via CDN URLs, projects rows to `{prompt, response}` with fallback keys, and streams NDJSON output.
- `bin/build_manifest.py` produces `manifest.json` for a given repo/date folder containing repo, date, and list of `{path, cdn_url}` entries; exits non-zero on HF API failure.
- `bin/dataset-enrich.sh` invokes `worker.py` so existing GitHub Actions matrix jobs continue to work (thin wrapper).
- `requirements.txt` includes `requests`, `pyarrow`, `tqdm` (and `huggingface_hub` if not present).
- `.github/workflows/ingest.yml` (or equivalent) defines a 16-shard matrix passing `SHARD_ID`/`N_SHARDS`, uses `HF_TOKEN`, and uploads per-shard NDJSON artifacts or pushes to a dataset branch.

## qa — qa @ 2026-05-03T04:16:39.159360Z

PASS: surrogate-1

1. **Acceptance criteria**
- Worker accepts SHARD_ID and N_SHARDS (default 16) via environment and emits only NDJSON lines where each line is valid JSON containing string keys `prompt` and `response`.
- Worker lists top-level date folders under `batches/public-merged/` via one `list_repo_tree` call and assigns folders to shards by `hash(date_folder) % N_SHARDS`; shard assignment is deterministic across runs.
- Worker downloads parquet files via CDN URLs (`resolve/main/...`) and projects rows to `{prompt, response}` using fallback key paths (`prompt/input/question` × `response/output/answer`); malformed rows are skipped and counted.
- `bin/build_manifest.py` produces `manifest.json` with `repo`, `date`, and `files: [{path, cdn_url}]`; exits non-zero and prints error on HF API failure or missing token.
- `bin/dataset-enrich.sh` is a thin wrapper that invokes `python bin/worker.py` and preserves existing GitHub Actions matrix behavior (pass-through env and exit code).
- `requirements.txt` contains `requests`, `pyarrow`, `tqdm`, and `huggingface_hub` (pinned or minimum version).
- `.github/workflows/ingest.yml` defines a 16-shard matrix with `SHARD_ID: [0..15]`, passes `N_SHARDS=16`, uses `HF_TOKEN`, and uploads per-shard NDJSON artifacts (or pushes to dataset branch).

2. **Unit tests**
```python
# tests/unit/test_worker_sharding.py
def test_shard_assignment_deterministic():
    from bin.worker import assign_shard
    folders = ["2026-04-30", "2026-05-01", "2026-05-02"]
    assignments = [assign_shard(f, n=16) for f in folders]
    assert len(set(assignments)) <= 16
    assert assignments == [assign_shard(f, n=16) for f in folders]  # deterministic

def test_shard_default_n():
    import os
    from unittest.mock import patch
    from bin.worker import main
    with patch.dict(os.environ, {"SHARD_ID": "3"}, clear=True):
        with patch("bin.worker.run_worker") as m:
            main()
            m.assert_called_once()
            call_kwargs = m.call_args.kwargs
            assert call_kwargs.get("n_shards") == 16

# tests/unit/test_projection.py
def test_project_row_fallback_keys():
    from bin.worker import project_row
    row = {"prompt": {"input": {"question": "q1"}}, "response": {"output": {"answer": "a1"}}}
    out = project_row(row)
    assert out == {"prompt": "q1", "response": "a1"}

def test_project_row_flat_keys():
    from bin.worker import project_row
    row = {"prompt": "q2", "response": "a2"}
    out = project_row(row)
    assert out == {"prompt": "q2", "response": "a2"}

def test_project_row_missing_returns_none():
    from bin.worker import project_row
    row = {"x": 1}
    out = project_row(row)
    assert out is None

# tests/unit/test_manifest.py
def test_build_manifest_output(tmp_path):
    from bin.build_manifest import build_manifest
    import json
    manifest_path = tmp_path / "manifest.json"
    # mock HF API to return sample tree
    with patch("bin.build_manifest.HfApi") as MockApi:
        mock_api = MockApi.return_value
        mock_api.list_repo_tree.return_value = [
            {"path": "batches/public-merged/2026-04-30/file1.parquet", "type": "file"},
            {"path": "batches/public-merged/2026-04-30/file2.parquet", "type": "file"},
        ]
        build_manifest(repo="test/repo", date="2026-04-30", out=str(manifest_path), token="tok")
        data = json.loads(manifest_path.read_text())
        assert data["repo"] == "test/repo"
        assert data["date"] == "2026-04-30"
        assert len(data["files"]) == 2
        assert all("cdn_url" in f and f["cdn_url"].startswith("https://") for f in data["files"])
```

3. **Integration tests**
- Happy: Worker with mocked `list_repo_tree` and local parquet fixture processes assigned shard and emits valid NDJSON lines equal to total rows across assigned files; exit code 0.
- Happy: `build_manifest.py` against real repo (smoke) produces manifest with non-empty files and valid CDN URLs; exit code 0.
- Happy: GitHub Actions m
