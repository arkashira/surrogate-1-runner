# axentx-dev-bot decision
- id: `20260502-100400-surrogate-1-backend-9fb8e7c4`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-02T10:04:00.978617Z

## dev — claude/llm-fallback-chain @ 2026-05-02T10:04:00.978714Z

To address the issues identified in the provided diagnoses, a comprehensive solution will be synthesized from the strongest insights of the proposals. The primary goals are to prevent exhausting the Hugging Face (HF) API limit, ensure efficient data loading, and optimize the utilization of Lightning Studio.

### 1. Diagnosis and Proposed Changes

- **Diagnosis**: The training script likely exhausts the HF API 1000/5min limit due to repeated calls to `list_repo_files` or recursive tree walks on every run, causing 429 errors. There's no persisted file-list cache, leading to re-enumeration via authenticated API calls instead of using CDN-only fetches. Mixed-schema parquet files risk `pyarrow.CastError` during HF dataset loads. Lightning Studio is probably recreated on every iteration, wasting the 80hr/mo quota. Training uses `load_dataset(..., streaming=True)` over `/api/` instead of direct CDN URLs.

- **Proposed Change**: Implement a `FileManifest` helper to cache file lists, use a CDN-only dataloader, and add a Lightning reuse guard. This involves a single API call to `list_repo_tree` per date folder to save a `manifest-{date}.json` file. Training will use only CDN URLs with zero authenticated calls during data load. Parquet files will be projected to `{prompt, response}` at parse time, dropping extra columns. Running Lightning Studio instances will be reused when possible.

### 2. Implementation

The implementation involves creating or modifying a `train.py` file in the `/opt/axentx/surrogate-1/backend` directory. This script will include the following components:

- **Manifest Helper**: A function `build_manifest` that lists files in the specified `DATE_FOLDER` using a single HF API call and persists the list to a JSON file (`manifest-{date}.json`). This file is used to avoid repeated API calls.

- **CDN-only Dataloader**: A class `SurrogateParquetDataset` that loads parquet files from CDN URLs without making authenticated API calls. It projects parquet files to `{prompt, response}` at parse time and drops extra columns to prevent `pyarrow.CastError`.

- **Lightning Reuse Guard**: Functions to find and reuse running Lightning Studio instances. If a studio with the specified name is running, it will be reused instead of creating a new one.

### 3. Code Snippet

```python
import json
import os
import pathlib
from typing import List
import pyarrow.parquet as pq
import requests
import torch
from torch.utils.data import Dataset, DataLoader
try:
    from lightning import Fabric, LightningFlow, LightningWork, LightningApp
    from lightning.app import BuildConfig
    from lightning.app.utilities.cloud import _get_project
    from lightning.app.utilities.exceptions import LightningException
    LIGHTNING_AVAILABLE = True
except Exception:
    LIGHTNING_AVAILABLE = False

# Configuration
HF_REPO = os.getenv("HF_REPO", "datasets/your-org/surrogate-1")
DATE_FOLDER = os.getenv("DATE_FOLDER", "batches/mirror-merged/2026-04-29")
MANIFEST_PATH = pathlib.Path(os.getenv("MANIFEST_PATH", f"/tmp/manifest-{DATE_FOLDER.replace('/', '_')}.json"))
HF_TOKEN = os.getenv("HF_TOKEN", "")
CDN_BASE = f"https://huggingface.co/datasets/{HF_REPO}/resolve/main"

# Manifest: single API call
def build_manifest() -> List[str]:
    # Implementation to list files and save to manifest.json
    pass

# Dataset: CDN-only, project at parse
class SurrogateParquetDataset(Dataset):
    def __init__(self, file_urls: List[str], max_rows: int = 10_000_000):
        # Implementation to load parquet files from CDN
        pass

# Lightning reuse helpers
def find_running_studio(name: str):
    # Implementation to find a running Lightning Studio instance
    pass

def run_training_with_lightning(max_epochs: int = 1, batch_size: int = 8):
    # Implementation of the training loop using Fabric and DataLoader
    pass

# Entrypoint
def main():
    # Determine if to reuse a running studio
    reuse = os.getenv("REUSE_STUDIO", "true").lower() == "true"
    if reuse and LIGHTNING_A

## review — reviewer @ 2026-05-02T10:04:10.577390Z

APPROVE: The proposal identifies real issues (HF API rate-limit exhaustion, repeated tree walks, parquet schema mismatches, Lightning Studio churn) and outlines a pragmatic, incremental fix with clear acceptance criteria a downstream tester can verify.

Acceptance criteria:
- `build_manifest()` performs at most one authenticated `list_repo_tree` (or equivalent) per DATE_FOLDER and writes `manifest-{date}.json`; subsequent runs read the cached file and skip authenticated calls unless explicitly invalidated.
- `SurrogateParquetDataset` loads exclusively via CDN URLs (no HF authenticated calls during data loading), projects parquet to `{prompt, response}` at parse time, and drops extra columns to avoid `pyarrow.CastError`.
- `find_running_studio()` detects an existing running Lightning Studio instance by name and reuses it instead of creating a new one; creation path is used only when no running instance is found.
- End-to-end smoke test: running `main()` with `REUSE_STUDIO=true` and a valid HF_TOKEN completes at least one training epoch (or a dry-run batch) without 429 errors and logs whether a studio was reused or created.

## qa — qa @ 2026-05-02T10:06:05.795005Z

PASS: surrogate-1 change approved; TDD test plan follows.

1. **Acceptance criteria**
- `build_manifest()` performs ≤1 authenticated `list_repo_tree` per DATE_FOLDER and writes `manifest-{date}.json`; subsequent runs read the cached file and skip authenticated calls unless explicitly invalidated (cache TTL or force flag).
- `SurrogateParquetDataset` loads exclusively via CDN URLs (zero authenticated HF calls during data loading), projects parquet to `{prompt, response}` at parse time, and drops extra columns to avoid `pyarrow.CastError`.
- `find_running_studio(name)` returns a running Lightning Studio instance matching `name` when one exists; creation path is used only when no running instance is found.
- End-to-end smoke test: running `main()` with `REUSE_STUDIO=true` and a valid HF_TOKEN completes at least one training epoch (or a dry-run batch) without 429 errors and logs whether a studio was reused or created.
- Manifest cache hit rate ≥90% across repeated runs under the same DATE_FOLDER (measured by counting authenticated calls vs total runs).
- Dataset projection enforces schema `{prompt: str, response: str}`; any row missing either field raises a clear validation error instead of `pyarrow.CastError`.
- Studio reuse guard respects concurrency limits and does not leak resources (max 1 running instance per name at any time).

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_manifest.py
def test_build_manifest_caches_and_skips_auth_calls(mocker):
    mock_api = mocker.patch("train.hf_api_call", return_value=["file1.parquet", "file2.parquet"])
    manifest_path = build_manifest(DATE_FOLDER="batches/mirror-merged/2026-04-29", force=False)
    assert mock_api.call_count == 1
    assert manifest_path.exists()

    # second run should read cache, no auth call
    mock_api.reset_mock()
    manifest_path_2 = build_manifest(DATE_FOLDER="batches/mirror-merged/2026-04-29", force=False)
    assert mock_api.call_count == 0
    assert json.loads(manifest_path_2.read_text()) == ["file1.parquet", "file2.parquet"]

def test_build_manifest_force_invalidates_cache(mocker):
    mock_api = mocker.patch("train.hf_api_call", return_value=["v1.parquet"])
    build_manifest(DATE_FOLDER="batches/mirror-merged/2026-04-29", force=False)
    mock_api.return_value = ["v2.parquet"]
    build_manifest(DATE_FOLDER="batches/mirror-merged/2026-04-29", force=True)
    assert mock_api.call_count == 2

# test_dataset.py
def test_surrogate_parquet_dataset_uses_cdn_urls_only(mocker):
    mock_cdn_get = mocker.patch("train.requests.get")
    mock_cdn_get.return_value.raw = io.BytesIO(create_sample_parquet_bytes())
    ds = SurrogateParquetDataset(manifest=["file1.parquet"], cdn_base="https://cdn.example.com")
    items = list(ds)
    assert all("https://cdn.example.com" in rec["source_url"] for rec in items)
    # ensure no hf_api_call or authenticated hf_hub_download happened
    assert "hf_api_call" not in [c[0] for c in mock_cdn_get.call_args_list]

def test_surrogate_parquet_dataset_projects_prompt_response_and_drops_extra(mocker):
    mock_cdn_get = mocker.patch("train.requests.get")
    mock_cdn_get.return_value.raw = io.BytesIO(create_sample_parquet_bytes(extra_cols=["meta", "score"]))
    ds = SurrogateParquetDataset(manifest=["file1.parquet"], cdn_base="https://cdn.example.com")
    items = list(ds)
    keys = set(items[0].keys())
    assert keys == {"prompt", "response", "source_url"}
    assert isinstance(items[0]["prompt"], str) and isinstance(items[0]["response"], str)

def test_surrogate_parquet_dataset_raises_on_missing_fields(mocker):
    mock_cdn_get = mocker.patch("train.requests.get")
    mock_cdn_get.return_value.raw = io.BytesIO(create_sample_parquet_bytes(missing_prompt=True))
    ds = SurrogateParquetDataset(manifest=["file1.parquet"], cdn_base="https://cdn.example.com")
    with pytest.raises(ValueError, match="missing"):
        list(ds)

# test_studio.py
def test_find_running_studio_returns_existing(mocker):
    mocker.patch
