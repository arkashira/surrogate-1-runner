# axentx-dev-bot decision
- id: `20260503-005323-surrogate-1-discovery-d72dccc3`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:53:23.146472Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:53:23.146527Z

To synthesize the best parts of multiple AI proposals and combine the strongest insights into one final answer, let's analyze the provided information and resolve any contradictions in favor of correctness and concrete actionability.

The primary goal here is to implement a solution that allows for the efficient and deterministic loading of data for training, specifically by utilizing a Mac-side tool to generate a `file_manifest.json` for a Hugging Face dataset. This manifest contains CDN URLs and metadata, enabling zero-API fetches during data loading, thus bypassing the need for repeated API calls and preventing 429 errors during long training runs.

### Synthesized Implementation Plan

1. **Create `tools/snapshot_manifest.py`**:
   - This script will accept parameters such as `--repo`, `--date`, and an optional `--out` for specifying the output file path.
   - It makes a single `list_repo_tree` call to the Hugging Face API for the specified repository under a given date partition.
   - The script generates a `file_manifest.json` containing necessary metadata (e.g., `generated_at`, `snapshot_id`, `repo`, `date`, `files` with `path`, `size`, `etag`, `cdn_url`, and a `shard_map` for deterministic shard assignment).
   - The `cdn_url` is constructed using a template to directly access files via the CDN, reducing the need for API calls during training.

2. **Implement `tools/verify_manifest.py`**:
   - This lightweight tool validates the schema of the generated `file_manifest.json`.
   - Optionally, it can perform a HEAD check on the CDN URLs listed in the manifest to ensure they are reachable, with a configurable timeout.

3. **Update Training Launcher**:
   - Modify the training script (e.g., `train.py` or a Lightning script) to read the `file_manifest.json`.
   - Implement an `IterableDataset` that downloads files directly from the CDN URLs provided in the manifest, utilizing streaming and `Range` requests for efficiency.
   - Ensure deterministic shard selection based on the `shard_id` and `world_size` to facilitate parallel training.

4. **Add to Repository**:
   - Include the necessary dependencies in `requirements-dev.txt`.
   - Place the `tools/` directory with `__main__` entry points for `snapshot_manifest.py` and `verify_manifest.py`.
   - Document the usage and purpose of these tools in `tools/README.md`.

5. **Smoke Test**:
   - Run `snapshot_manifest.py` for a recent date partition.
   - Verify that the generated manifest contains CDN URLs and is correctly formatted.
   - Perform a mini-training run with a small sample to confirm that data is loaded correctly from the CDN without making API calls.

### Estimated Time and Actionability

The estimated time for implementing these steps is approximately 120 minutes, considering coding, testing, and documentation. This plan is actionable because it:

- Directly addresses the need to reduce API calls during training.
- Provides a clear, step-by-step approach to implementation.
- Includes tools for validation and verification of the manifest and CDN URLs.
- Enhances the efficiency and determinism of data loading for training.

By following this synthesized plan, developers can efficiently implement a solution that bypasses the Hugging Face API for data loading during training, reducing the likelihood of 429 errors and improving overall training efficiency.

## review — reviewer @ 2026-05-03T00:53:54.610394Z

APPROVE: This is a workable, concrete first step that directly addresses the 429/API-rate bottleneck with deterministic CDN-backed data loading; it proposes specific tools, entry points, and a smoke test that a downstream tester can validate.

Acceptance criteria:
- `tools/snapshot_manifest.py` exists with `--repo`, `--date`, `--out` CLI options and produces a valid `file_manifest.json` containing `generated_at`, `snapshot_id`, `repo`, `date`, `files[]` (path, size, etag, cdn_url), and a `shard_map`.
- `tools/verify_manifest.py` exists with a schema validator for the manifest and an optional HEAD-check mode for CDN URLs (configurable timeout) that exits non-zero on invalid schema/unreachable URLs.
- Training launcher (e.g., `train.py` or equivalent) can accept a `--manifest` path and uses an `IterableDataset` that streams from CDN URLs with Range requests and deterministic shard selection via `shard_id`/`world_size`.
- `requirements-dev.txt` includes any new runtime deps (e.g., `requests`, `tqdm`, `hf` client) and `tools/__main__.py` (or console-scripts) exposes `snapshot_manifest` and `verify_manifest` entry points.
- Smoke test passes: running snapshot for a recent partition produces a non-empty manifest with CDN URLs, and a mini-training run over a small sample completes without Hugging Face API calls (verified via logging or network inspection).

## qa — qa @ 2026-05-03T00:55:48.403178Z

PASS: Proceed with implementation.

1. **Acceptance criteria**
- `tools/snapshot_manifest.py` exists and accepts `--repo`, `--date`, `--out`; produces a valid `file_manifest.json` containing `generated_at` (ISO-8601), `snapshot_id` (UUID), `repo` (string), `date` (YYYY-MM-DD), `files[]` (each with `path`, `size` ≥ 0, `etag`, `cdn_url`), and `shard_map` (dict mapping shard_id → file list).
- `tools/verify_manifest.py` exists and validates manifest schema; with `--check-cdn` performs HEAD requests with configurable `--timeout` and exits non-zero on invalid schema or any unreachable CDN URL.
- Training launcher accepts `--manifest <path>` and uses an `IterableDataset` that streams via HTTP Range requests from `cdn_url`, with deterministic shard selection using `shard_id` and `world_size` (each shard disjoint and covering all files exactly once).
- `requirements-dev.txt` includes `requests`, `tqdm`, `hf-transfer` or `huggingface-hub`, and `tools/__main__.py` (or equivalent console-scripts) exposes `snapshot_manifest` and `verify_manifest` as runnable commands.
- Smoke test passes: snapshot for a recent partition yields non-empty manifest with valid CDN URLs; mini-training run over a small sample completes without Hugging Face API calls (verified via logs/network capture showing zero calls to api.huggingface.co datasets endpoints).

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_snapshot_manifest.py
def test_cli_parses_required_args():
    args = parse_args(["--repo", "my/repo", "--date", "2024-06-01", "--out", "out.json"])
    assert args.repo == "my/repo"
    assert args.date == "2024-06-01"
    assert args.out == "out.json"

def test_build_cdn_url():
    url = build_cdn_url("my/repo", "data/train-00001.parquet")
    assert url.startswith("https://cdn-lfs") or "huggingface.co" in url
    assert "data/train-00001.parquet" in url

def test_generate_manifest_structure(tmp_path):
    out = tmp_path / "manifest.json"
    manifest = generate_manifest(repo="my/repo", date="2024-06-01", tree=sample_tree())
    manifest_to_file(manifest, out)
    data = json.loads(out.read_text())
    assert "generated_at" in data and "snapshot_id" in data
    assert data["repo"] == "my/repo"
    assert data["date"] == "2024-06-01"
    assert isinstance(data["files"], list) and len(data["files"]) > 0
    for f in data["files"]:
        assert "path" in f and isinstance(f["size"], int) and f["size"] >= 0
        assert "etag" in f and "cdn_url" in f
    assert "shard_map" in data and isinstance(data["shard_map"], dict)

def test_shard_map_deterministic():
    files = [{"path": f"file-{i}.bin", "size": 100} for i in range(10)]
    shard_map = build_shard_map(files, world_size=4)
    assigned = [f for shard in shard_map.values() for f in shard]
    assert sorted(assigned, key=lambda x: x["path"]) == sorted(files, key=lambda x: x["path"])
    for shard in shard_map.values():
        assert len(shard) in (2, 3)  # balanced
```

```python
# tests/unit/test_verify_manifest.py
def test_valid_manifest_passes_schema():
    assert validate_manifest(sample_valid_manifest()) is True

def test_invalid_manifest_fails_schema():
    with pytest.raises(ValidationError):
        validate_manifest({"files": "not-a-list"})

def test_head_check_reachable_urls(requests_mock):
    requests_mock.head("https://cdn.example/file1", status_code=200)
    ok, fails = check_cdn_urls([{"cdn_url": "https://cdn.example/file1"}], timeout=2)
    assert ok is True and len(fails) == 0

def test_head_check_unreachable_url(requests_mock):
    requests_mock.head("https://cdn.example/bad", status_code=404)
    ok, fails = check_cdn_urls([{"cdn_url": "https://cdn.example/bad"}], timeout=2)
    assert ok is False and len(fails) == 1
```

```python
# tests/unit/test_dataset.py
def test_shard_selection_deterministic():
    manifest = sample_valid_manifest()
    world_size, shard_id = 4, 1
    ds = CDNIterableDataset(manifest, shard_id=shard_id, world_size=world_size)
    assi
