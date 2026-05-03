# axentx-dev-bot decision
- id: `20260503-044742-surrogate-1-discovery-80d5eb21`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T04:47:42.013302Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:47:42.013415Z

# Final Synthesis — Manifest-Driven Ingestion (Correct + Actionable)

## Core improvement (≤2h)
Replace fragile shell-based ingestion with a **manifest-driven, CDN-bypass Python worker** that:
- Eliminates HF API rate limits during training data load by fetching via CDN-only URLs (`resolve/main/...`).
- Prevents mixed-schema `CastError`s by projecting to `{prompt, response}` at parse time.
- Produces deterministic shard outputs compatible with existing `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl` layout.
- Keeps the 16-shard matrix workflow intact (only changes worker + adds manifest generator).

---

## Implementation plan (≤2h)

| Step | Owner | Time | Description |
|------|-------|------|-------------|
| 1 | Me | 10m | Add `requirements.txt` updates (`requests`, `tqdm`; keep `pyarrow`, `datasets`, `huggingface_hub`). |
| 2 | Me | 20m | Create `bin/generate_manifest.py` — run once per date folder to list files via `list_repo_tree(recursive=False)` and emit `manifest-<date>.json`. |
| 3 | Me | 40m | Replace `bin/dataset-enrich.sh` with `bin/worker.py` (manifest-driven, CDN-only, schema projection, dedup via `lib/dedup.py`). |
| 4 | Me | 15m | Update `.github/workflows/ingest.yml` to pass `MANIFEST_PATH` and run `python bin/worker.py` with `SHARD_ID`/`SHARD_TOTAL`. |
| 5 | Me | 15m | Add smoke test + local run instructions; ensure executables and shebangs for any remaining shell helpers. |

Total: ~1h 40m.

---

## Code snippets

### 1) requirements.txt (additions)

```text
# existing
datasets
huggingface_hub
pyarrow
numpy

# new
requests>=2.31
tqdm>=4.66
```

---

### 2) bin/generate_manifest.py

Run once per date folder (locally or in workflow) to produce a manifest. Uses HF API sparingly (one tree call per folder) and avoids recursive listing of large repos.

```python
#!/usr/bin/env python3
"""
Generate manifest for a date folder in axentx/surrogate-1-training-pairs.

Usage:
  HF_TOKEN=<token> python bin/generate_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --out manifest-2026-05-03.json

Output manifest format:
{
  "repo": "...",
  "date": "...",
  "files": [
    {"path": "batches/public-merged/2026-05-03/file1.parquet", "size": 12345},
    ...
  ]
}
"""
import argparse
import json
import os
import sys
from typing import Dict, List

from huggingface_hub import HfApi, login

def build_manifest(repo_id: str, date: str, folders: List[str]) -> Dict:
    api = HfApi()
    files = []
    for folder in folders:
        try:
            tree = api.list_repo_tree(repo_id=repo_id, path=folder, repo_type="dataset")
        except Exception as exc:
            print(f"Warning: failed to list {folder}: {exc}", file=sys.stderr)
            continue
        for item in tree:
            if item.rfilename and not item.rfilename.endswith("/"):
                files.append({
                    "path": item.rfilename,
                    "size": item.size or 0,
                })
    manifest = {
        "repo": repo_id,
        "date": date,
        "folders": folders,
        "files": files,
    }
    return manifest

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate manifest for a date folder.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-03")
    parser.add_argument("--folders", nargs="+", default=None,
                        help="Folders to scan (default: batches/public-merged/<date>)")
    parser.add_argument("--out", required=True, help="Output manifest JSON path")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if token:
        login(token=token, add_to_git_credential=False)

    folders = args.folders or [f"batches/public-merged/{args.date}"]
    manifest = build_manifest(args.repo, args.date, folders)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(

## review — reviewer @ 2026-05-03T04:47:48.066182Z

APPROVE — this is a workable, incremental step that replaces fragile shell ingestion with a manifest-driven Python worker, eliminates HF API rate limits via CDN URLs, prevents `CastError` by projecting schema early, and preserves the 16-shard matrix. It has clear acceptance criteria a downstream tester can validate.

Acceptance criteria:
- `bin/generate_manifest.py` produces valid JSON with `repo`, `date`, `folders`, and `files[].path/size` for a given date folder.
- `bin/worker.py` deterministically assigns files to shards via `hash(path) % SHARD_TOTAL == SHARD_ID` and emits `shard<N>-<HHMMSS>.jsonl` in the expected layout.
- Worker fetches via CDN-only URLs (e.g., `https://huggingface.co/datasets/<repo>/resolve/main/<path>`) without requiring HF API auth for reads.
- Worker projects each row to `{prompt, response}` and runs deduplication via `lib/dedup.py` before writing output.
- Workflow `.github/workflows/ingest.yml` sets `MANIFEST_PATH`, `SHARD_ID`, `SHARD_TOTAL`, and runs `python bin/worker.py` successfully in CI.

## review — qa @ 2026-05-03T04:48:06.679251Z

PASS: Manifest-driven ingestion plan is workable and testable.

1. **Acceptance criteria**
- bin/generate_manifest.py exits 0 and emits valid JSON containing repo, date, folders, and files[].{path,size} for a supplied date folder.
- bin/worker.py deterministically assigns files to shards via hash(path) % SHARD_TOTAL == SHARD_ID and produces shard<N>-<HHMMSS>.jsonl in batches/public-merged/<date>/ with one JSON object per line.
- Worker fetches every file via CDN-only URLs (https://huggingface.co/datasets/<repo>/resolve/main/<path>) and does not require HF API auth tokens for read operations.
- Worker projects each input row to {prompt, response} and removes duplicates via lib/dedup.py before writing; output rows strictly contain only those two keys.
- Workflow .github/workflows/ingest.yml sets MANIFEST_PATH, SHARD_ID, SHARD_TOTAL and runs python bin/worker.py successfully (exit 0) in CI with no HF API rate-limit failures.

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_generate_manifest.py
def test_manifest_schema():
    manifest = generate_manifest(repo="axentx/surrogate-1-training-pairs", date="2026-05-03", folders=["batches/public-merged/2026-05-03"])
    assert "repo" in manifest and isinstance(manifest["repo"], str)
    assert "date" in manifest and manifest["date"] == "2026-05-03"
    assert "folders" in manifest and isinstance(manifest["folders"], list)
    assert "files" in manifest and isinstance(manifest["files"], list)
    for f in manifest["files"]:
        assert "path" in f and isinstance(f["path"], str)
        assert "size" in f and isinstance(f["size"], int) and f["size"] >= 0

def test_manifest_roundtrip_json(tmp_path):
    out = tmp_path / "manifest.json"
    main(["--repo", "axentx/surrogate-1-training-pairs", "--date", "2026-05-03", "--out", str(out)])
    data = json.loads(out.read_text())
    assert data["date"] == "2026-05-03"

# tests/unit/test_worker_sharding.py
def test_shard_assignment_deterministic():
    paths = ["batches/public-merged/2026-05-03/a.parquet", "batches/public-merged/2026-05-03/b.parquet"]
    total = 16
    assignments = [shard_id_for(path, total) for path in paths]
    for path, assigned in zip(paths, assignments):
        assert assigned == hash(path) % total

def test_worker_filters_by_shard_id():
    manifest = {"files": [{"path": "batches/public-merged/2026-05-03/a.parquet"}, {"path": "batches/public-merged/2026-05-03/b.parquet"}]}
    selected = select_files_for_shard(manifest, shard_id=3, shard_total=16)
    for f in selected:
        assert shard_id_for(f["path"], 16) == 3

# tests/unit/test_schema_projection.py
def test_project_to_prompt_response():
    row = {"prompt": "hello", "response": "world", "extra": 123}
    projected = project_row(row)
    assert set(projected.keys()) == {"prompt", "response"}
    assert projected["prompt"] == "hello"
    assert projected["response"] == "world"

# tests/unit/test_cdn_urls.py
def test_cdn_url_generation():
    url = cdn_url(repo="axentx/surrogate-1-training-pairs", path="batches/public-merged/2026-05-03/a.parquet")
    assert url.startswith("https://huggingface.co/datasets/")
    assert "/resolve/main/" in url
    assert "huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/batches/public-merged/2026-05-03/a.parquet" in url

# tests/unit/test_dedup_integration.py
def test_dedup_removes_identical_rows():
    rows = [{"prompt": "x", "response": "y"}, {"prompt": "x", "response": "y"}]
    deduped = dedup_rows(rows)
    assert len(deduped) == 1
```

3. **Integration tests** (3 happy + 3 edge)

Happy cases
- Manifest generation against real repo (read-only) produces non-empty manifest with valid file entries for a known date folder.
- Worker run with SHARD_TOTAL=16 and SHARD_ID=0 processes assigned files, downloads via CDN URLs, projects schema, deduplicates, and writes shard0-<timestamp>.jsonl containing only {prompt,response} rows.
- Full 16-shard local simulation (SHARD_TOTAL=16, SH
