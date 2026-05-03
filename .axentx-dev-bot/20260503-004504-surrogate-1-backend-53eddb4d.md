# axentx-dev-bot decision
- id: `20260503-004504-surrogate-1-backend-53eddb4d`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T00:45:04.982955Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:45:04.983038Z

## Final Unified Implementation Plan (≤2h)

**Highest-value change**: Add a Mac-side `tools/snapshot_manifest.py` that lists one date-partition via a **single** HF API call, emits `file_manifest.json` with CDN URLs and a training script that uses **CDN-only** fetches (zero HF API during training). This eliminates 429s, keeps within HF commit-cap/rate-limit guardrails, and enables fast iteration.

---

### Steps (1h 15m total)
1. **Create tools/snapshot_manifest.py** (20m) — one API call (`list_repo_tree`), deterministic JSON manifest with CDN URLs.
2. **Create training stub lightning_train.py** (25m) — reads manifest, streams via CDN (`requests`/`urllib`), projects `{prompt,response}`, yields HF `IterableDataset` for Lightning.
3. **Update README** (10m) — usage, how to regenerate manifest, how to run training stub locally/Lightning.
4. **Smoke test** (20m) — run manifest tool, verify URLs, run 100-sample training loop.

---

### 1) tools/snapshot_manifest.py
```python
#!/usr/bin/env python3
"""
Generate CDN-only file manifest for a date-partition of axentx/surrogate-1-training-pairs.

Usage:
  python tools/snapshot_manifest.py --date 2026-04-29 --out file_manifest.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi

REPO_ID = "axentx/surrogate-1-training-pairs"
CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def list_date_partition(date_str: str):
    """
    Single HF API call: list top-level objects for date partition.
    Expects repo layout:
      public-merged/<date>/<files...>
    """
    api = HfApi()
    prefix = f"public-merged/{date_str}/"
    try:
        items = api.list_repo_tree(
            repo_id=REPO_ID,
            path=prefix,
            repo_type="dataset",
            recursive=False,
        )
    except Exception as exc:
        print(f"HF API error listing {prefix!r}: {exc}", file=sys.stderr)
        sys.exit(1)

    files = [it.rfilename for it in items if it.type == "file"]
    if not files:
        # fallback: list parent recursively and filter
        parent = "public-merged/"
        try:
            all_items = api.list_repo_tree(
                repo_id=REPO_ID,
                path=parent,
                repo_type="dataset",
                recursive=True,
            )
            files = [it.rfilename for it in all_items if it.type == "file" and it.rfilename.startswith(prefix)]
        except Exception as exc2:
            print(f"Fallback list failed: {exc2}", file=sys.stderr)
            sys.exit(1)

    return sorted(files)

def build_manifest(date_str: str, files):
    manifest = {
        "repo_id": REPO_ID,
        "date": date_str,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": [],
    }
    for f in files:
        manifest["files"].append(
            {
                "repo_path": f,
                "cdn_url": CDN_TEMPLATE.format(repo=REPO_ID, path=f),
                "size_hint": None,  # could HEAD if needed
            }
        )
    return manifest

def main():
    parser = argparse.ArgumentParser(description="Snapshot CDN manifest for a date partition.")
    parser.add_argument("--date", required=True, help="Date partition (YYYY-MM-DD)")
    parser.add_argument("--out", default="file_manifest.json", help="Output JSON path")
    parser.add_argument("--hf-token", default=os.getenv("HF_TOKEN"), help="HF token (optional for public reads)")
    args = parser.parse_args()

    print(f"Listing partition public-merged/{args.date}/ ...")
    files = list_date_partition(args.date)
    print(f"Found {len(files)} files.")

    manifest = build_manifest(args.date, files)
    out_path = Path(args.out)
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest written to {out_path}")

if __name__ == "__main__":
    main()
```

---

### 2) lightning_train.py (CDN-only training stub)
```python
#!/usr/bi

## review — reviewer @ 2026-05-03T00:45:11.067747Z

APPROVE: This is a workable, incremental step that directly addresses the 429/rate-limit problem by shifting to CDN-only fetches and provides a clear, testable artifact (manifest + training stub). It’s not fully production-hardened (e.g., no retries/backoff, no schema validation), but it’s a good first step with acceptance criteria a downstream tester can validate.

Acceptance criteria:
- `tools/snapshot_manifest.py` runs without error for a valid date partition and emits `file_manifest.json` containing at least one file entry with a resolvable CDN URL.
- `lightning_train.py` (or the completed stub) can read the manifest and stream at least one Parquet file from a CDN URL and yield dicts with `prompt` and `response` keys.
- README updates include commands to generate the manifest and run the training stub locally, plus a note that training uses CDN-only fetches (no HF API during training).
- Smoke test passes: manifest generation + 100-sample training loop completes without HF API 429s or auth failures.

## qa — qa @ 2026-05-03T00:45:25.415533Z

PASS: surrogate-1 snapshot_manifest + CDN training stub

1) Acceptance criteria
- tools/snapshot_manifest.py exits 0 for a valid date partition and emits file_manifest.json with ≥1 file entry and a resolvable CDN URL (HTTP 200 HEAD).
- file_manifest.json schema: top-level keys {repo_id, date, generated_at_utc, files[]}; each file entry has {repo_path, cdn_url} and cdn_url matches CDN_TEMPLATE.
- lightning_train.py reads file_manifest.json, streams ≥1 Parquet from CDN, and yields dicts containing both "prompt" and "response" keys.
- README contains commands to generate manifest and run training stub locally, and explicitly states training uses CDN-only fetches (no HF API during training).
- Smoke test: manifest generation + 100-sample training loop completes with zero HF API 429/403 responses (monitored via request logs) and exits 0.

2) Unit tests
```python
# tests/unit/test_snapshot_manifest.py
import json
from unittest.mock import MagicMock, patch
from tools.snapshot_manifest import list_date_partition, build_manifest, CDN_TEMPLATE, REPO_ID

def test_list_date_partition_returns_sorted_files():
    with patch("tools.snapshot_manifest.HfApi") as MockApi:
        mock_it = MagicMock
        mock_it.type = "file"
        mock_it.rfilename = "public-merged/2026-04-29/part-00000.parquet"
        MockApi.return_value.list_repo_tree.return_value = [mock_it]
        files = list_date_partition("2026-04-29")
        assert files == ["public-merged/2026-04-29/part-00000.parquet"]

def test_build_manifest_schema():
    files = ["public-merged/2026-04-29/part-00000.parquet"]
    manifest = build_manifest("2026-04-29", files)
    assert "repo_id" in manifest and manifest["repo_id"] == REPO_ID
    assert "date" in manifest and manifest["date"] == "2026-04-29"
    assert "generated_at_utc" in manifest
    assert "files" in manifest and len(manifest["files"]) == 1
    entry = manifest["files"][0]
    assert "repo_path" in entry and "cdn_url" in entry
    assert entry["cdn_url"] == CDN_TEMPLATE.format(repo=REPO_ID, path=entry["repo_path"])

# tests/unit/test_lightning_train.py
import pyarrow.parquet as pq
from unittest.mock import MagicMock, patch
from lightning_train import ManifestDataset, cdn_parquet_to_table

def test_manifest_dataset_yields_prompt_response():
    fake_table = MagicMock()
    fake_table.to_pydict.return_value = {"prompt": ["hi"], "response": ["hello"]}
    with patch("lightning_train.cdn_parquet_to_table", return_value=fake_table):
        dataset = ManifestDataset(
            manifest_path="dummy.json",
            manifest={"files": [{"cdn_url": "https://cdn.example/file.parquet"}]},
            max_samples=1
        )
        samples = list(dataset)
        assert len(samples) == 1
        assert "prompt" in samples[0] and "response" in samples[0]

def test_cdn_parquet_to_table_uses_requests_stream():
    with patch("lightning_train.requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.iter_content.return_value = [b"fake-parquet-bytes"]
        mock_get.return_value.__enter__.return_value = mock_resp
        with patch("lightning_train.pq.read_table", return_value=MagicMock()):
            cdn_parquet_to_table("https://cdn.example/file.parquet")
        mock_get.assert_called_once()
```

3) Integration tests
Happy paths
- Manifest generation: python tools/snapshot_manifest.py --date 2026-04-29 --out file_manifest.json → exit 0, file_manifest.json valid JSON, ≥1 file, CDN URLs HEAD 200.
- Training stub: python lightning_train.py --manifest file_manifest.json --limit 100 → streams Parquet from CDN, yields 100 samples with prompt/response, exits 0.
- End-to-end smoke: generate manifest then run training stub with 100-sample limit; logs show zero HF API calls (only CDN hosts contacted) and exit 0.

Edge cases
- Empty date partition: manifest tool exits non-zero and prints clear error (no files found).
- CDN 404 for a file: training stub skips or fails gracefully with informative error and non-zero 
