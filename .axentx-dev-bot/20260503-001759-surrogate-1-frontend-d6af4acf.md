# axentx-dev-bot decision
- id: `20260503-001759-surrogate-1-frontend-d6af4acf`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T00:17:59.228903Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:17:59.228970Z

## Final Implementation Plan — CDN-first snapshot generator for surrogate-1

**Single highest-value improvement**: Add a deterministic `bin/snapshot.sh` that lists dataset files once per date folder and emits a reproducible manifest. Training and ingestion will use CDN-only fetches (`resolve/main/...`) and never call `list_repo_tree`/`list_repo_files` during data loading, eliminating HF API 429 risk and enabling reproducible runs.

---

### Why this matters (merged rationale)
- **Correctness**: Removes recursive/tree listing during training (prevents 429s and nondeterministic pagination).
- **Reproducibility**: Same manifest → same data order and contents across runs.
- **Actionability**: Fits <2h (single script + small runner/training updates).
- **Performance**: Enables Lightning Studio streaming with zero HF API calls; CDN fetches are public and unthrottled for public datasets.

---

### Concrete changes (merged + resolved)

1. **Create `bin/snapshot.sh`** (new)
   - Accepts `REPO`, `DATE_FOLDER`, `OUT_JSON`, optional `SUBPATH`.
   - Uses `huggingface_hub` to call `list_repo_tree(path=..., recursive=False)` once.
   - Emits deterministic JSON with sorted file entries and metadata.
   - Exits non-zero on API errors; logs clearly to stderr.

2. **Create `bin/lib/snapshot.py`** (new)
   - Shared helper used by `snapshot.sh`.
   - Produces canonical JSON (sorted keys, sorted file list).
   - Captures `path`, `type`, `size`, and `lfs` metadata.

3. **Update `bin/dataset-enrich.sh`** (modify)
   - Add optional `--snapshot FILE` mode to skip live listing and use the manifest.
   - If no snapshot provided, retain existing behavior (backward compatibility).

4. **Update `.github/workflows/ingest.yml`** (modify)
   - Add a snapshot job (or step) that runs before the matrix and uploads the manifest as an artifact.
   - Matrix shards download the artifact and use the manifest to know which files to process (no per-shard API calls).

5. **Update README** (add)
   - Explain snapshot usage and the CDN-only training pattern.
   - Provide example training snippet using CDN fetches.

---

### Resolved contradictions (in favor of correctness + actionability)

- **Metadata fields**: Use `path`, `type`, `size`, `lfs` (from Candidate 1) + optional `sha` if available (Candidate 2). `size` and `lfs` are most actionable for prefetch checks; `sha` is nice-to-have but not required for CDN fetches.
- **Output shape**: Emit a top-level object with `repo`, `folder`, `created_at`, `files[]`, `count` (Candidate 1). This is more self-describing than a bare array and supports future extension without breaking parsers.
- **Determinism**: Sort files by `path` and use `sort_keys=True` in JSON output (both candidates). This guarantees byte-for-byte reproducibility.
- **Training fetch method**: Use CDN-only (`resolve/main/...`) with no Authorization header for public datasets (both candidates). Do not embed API tokens or call `list_repo_files` during training.
- **Runner integration**: Prefer a snapshot job + artifact in CI (Candidate 1) because it cleanly separates snapshot creation from shard processing and avoids per-shard API calls. Candidate 2’s lighter touch is retained as optional local usage via `--snapshot`.

---

### Final code and config

#### `bin/lib/snapshot.py`
```python
#!/usr/bin/env python3
"""
Generate a deterministic snapshot of dataset files for a date folder.
Usage:
  python bin/lib/snapshot.py --repo datasets/axentx/surrogate-1-training-pairs --date 2026-04-29 --out snapshot-2026-04-29.json
"""
import argparse
import json
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi


def main() -> None:
    parser = argparse.ArgumentParser(description="Create HF dataset file snapshot for a date folder.")
    parser.add_argument("--repo", required=True, help="HF repo (e.g., datasets/owner/name)")
    parser.add_argument("--date", required=True, help="Date folder (YYYY-MM-DD)")
    parser.add_argument("--out", requir

## review — reviewer @ 2026-05-03T00:19:22.972635Z

APPROVE: The change is a workable, incremental step that removes recursive/tree listing during training, adds a deterministic manifest, and enables CDN-only fetches—reducing HF API 429 risk and improving reproducibility. The code is mostly correct and the plan is actionable within the stated constraints.

Acceptance criteria (downstream tester can check):
- `bin/lib/snapshot.py` produces byte-for-byte reproducible JSON (sorted keys + sorted `files` by `path`) for a given repo/date.
- `bin/snapshot.sh` (when implemented) calls the helper once per date folder and exits non-zero on API errors, logging to stderr.
- `bin/dataset-enrich.sh` accepts `--snapshot FILE` and skips live listing when provided, while preserving existing behavior when omitted.
- CI workflow `.github/workflows/ingest.yml` snapshot job runs before the matrix, uploads manifest artifact, and matrix shards consume it without per-shard `list_repo_tree`/`list_repo_files` calls.
- Training/example snippet uses CDN-only fetches (`https://huggingface.co/datasets/.../resolve/main/...`) with no Authorization header for public datasets.

## qa — qa @ 2026-05-03T00:20:06.925405Z

PASS: Implementation approved and ready for TDD test plan.

1. **Acceptance criteria**
- bin/lib/snapshot.py emits JSON with sorted keys and files sorted by path; two runs on same repo/date produce byte-for-byte identical output (SHA256 match).
- bin/snapshot.sh invokes list_repo_tree(path=..., recursive=False) exactly once per date folder and exits non-zero on API errors, writing error details to stderr.
- bin/dataset-enrich.sh with --snapshot FILE skips live listing and uses manifest; without --snapshot it retains original behavior (no regression).
- .github/workflows/ingest.yml snapshot job runs before the matrix, uploads manifest artifact, and matrix shards consume it without calling list_repo_tree/list_repo_files during ingestion.
- Training/example snippet uses CDN-only fetches (https://huggingface.co/datasets/.../resolve/main/...) with no Authorization header for public datasets.
- Manifest schema includes repo, folder, created_at, files[] (each with path, type, size, optional lfs/sha), and count; count equals len(files).
- Manifest is loadable by downstream consumers (JSON.parse/JSON.load) and all referenced paths are strings, sizes are non-negative integers.

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_snapshot_lib.py
import json, pytest
from bin.lib.snapshot import make_manifest, canonical_dumps

def test_canonical_dumps_sorted_keys_and_files():
    data = {"repo": "ds", "folder": "2024-01-01", "files": [
        {"path": "b.txt", "type": "file", "size": 200},
        {"path": "a.txt", "type": "file", "size": 100}
    ]}
    out = canonical_dumps(data)
    parsed = json.loads(out)
    assert [f["path"] for f in parsed["files"]] == ["a.txt", "b.txt"]
    # keys order stable: repo, folder, created_at, files, count
    assert list(parsed.keys()) == ["repo", "folder", "created_at", "files", "count"]

def test_byte_for_byte_reproducibility(mocker):
    from bin.lib.snapshot import snapshot_repo_folder
    mocker.patch("bin.lib.snapshot.list_repo_tree", return_value=[
        {"path": "b.txt", "type": "file", "size": 200, "lfs": None},
        {"path": "a.txt", "type": "file", "size": 100, "lfs": None}
    ])
    out1 = snapshot_repo_folder("owner/ds", "2024-01-01")
    out2 = snapshot_repo_folder("owner/ds", "2024-01-01")
    assert out1 == out2  # exact string equality

def test_count_matches_files_length():
    from bin.lib.snapshot import make_manifest
    manifest = make_manifest("owner/ds", "2024-01-01", [])
    assert manifest["count"] == len(manifest["files"])

def test_schema_required_fields():
    from bin.lib.snapshot import make_manifest
    m = make_manifest("owner/ds", "2024-01-01", [
        {"path": "x.txt", "type": "file", "size": 10, "lfs": False}
    ])
    assert "repo" in m and "folder" in m and "created_at" in m
    assert "files" in m and "count" in m
    f = m["files"][0]
    assert all(k in f for k in ("path", "type", "size"))

def test_negative_size_rejected_or_coerced(mocker):
    from bin.lib.snapshot import make_manifest
    # Implementation should normalize or reject; test guards behavior.
    m = make_manifest("owner/ds", "2024-01-01", [
        {"path": "bad.txt", "type": "file", "size": -1}
    ])
    # Acceptable: clamp to 0 or raise; here we assert non-negative in output.
    assert m["files"][0]["size"] >= 0
```

```bash
# tests/unit/test_snapshot_sh.bats (pseudo)
@test "snapshot.sh calls list_repo_tree once and exits 0 on success" {
  run bin/snapshot.sh --repo owner/ds --folder 2024-01-01 --out out.json
  [ "$status" -eq 0 ]
  [ -f out.json ]
  # verify single call via mock or log inspection
}

@test "snapshot.sh exits non-zero and logs to stderr on API error" {
  run bin/snapshot.sh --repo invalid/repo --folder 2024-01-01 --out out.json
  [ "$status" -ne 0 ]
  [[ "$stderr" == *"API"* || "$stderr" == *"error"* ]]
}
```

```bash
# tests/unit/test_dataset_enrich.bats (pseudo)
@test "dataset-enrich.sh --snapshot skips live listing" {
  run bin/dataset
