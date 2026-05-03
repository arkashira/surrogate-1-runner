# axentx-dev-bot decision
- id: `20260503-042229-surrogate-1-discovery-2a0f4bae`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T04:22:29.626342Z

## dev — claude/llm-fallback-chain @ 2026-05-03T04:22:29.626402Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Replace fragile shell-based ingestion with a **manifest-driven, CDN-bypass Python worker** that eliminates HF API rate limits during training data loads and prevents mixed-schema CastErrors.

### Changes

1. Add `bin/generate_manifest.py` — single Mac-side API call that lists one date folder via `list_repo_tree(recursive=False)` and writes `manifest.json` (file paths + sizes + etags + deterministic slugs). Embed this manifest in training scripts so Lightning workers do **CDN-only** fetches with zero API calls during data load.
2. Replace `bin/dataset-enrich.sh` with `bin/dataset_enrich.py` — deterministic shard assignment by slug hash, schema projection to `{prompt, response}` only, per-file `hf_hub_download` (bypass `load_dataset` mixed-schema CastError), streaming line-by-line to bound memory, and dedup via `lib/dedup.py`.
3. Add `requirements.txt` update (`requests` for CDN bypass) and lightweight GitHub Action step to generate+upload manifest before the 16-shard matrix runs.
4. Keep filename pattern `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` and HF commit-cap mitigation (128/hr) by deterministic shard → repo routing if needed.

Estimated time: 90 minutes (45m code, 30m test, 15m GH Action tweak).

---

### 1) Manifest generator (Mac side, run once per date folder)

`bin/generate_manifest.py`

```python
#!/usr/bin/env python3
"""
Generate manifest for a single date folder to enable CDN-only fetches.
Usage:
  HF_TOKEN=... python bin/generate_manifest.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-03 \
    --out manifest.json
"""
import argparse
import hashlib
import json
import os
import sys
from typing import Dict, List

from huggingface_hub import HfApi, login

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def slug_for_path(path: str) -> str:
    """Deterministic slug for dedup/sharding from repo-relative path."""
    return path.rstrip(".jsonl").rstrip(".parquet").replace("/", "_")

def build_manifest(repo: str, date: str) -> Dict:
    api = HfApi()
    folder = f"batches/public-merged/{date}"
    try:
        items = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    except Exception as exc:
        print(f"Failed to list {repo}/{folder}: {exc}", file=sys.stderr)
        sys.exit(1)

    files = []
    for item in items:
        if getattr(item, "type", None) != "file":
            continue
        path = item.path
        files.append(
            {
                "path": path,
                "slug": slug_for_path(path),
                "size": getattr(item, "size", None),
                "etag": getattr(item, "etag", None),
                "cdn_url": CDN_TEMPLATE.format(repo=repo, path=path),
            }
        )

    manifest = {
        "repo": repo,
        "date": date,
        "folder": folder,
        "generated_by": "generate_manifest.py",
        "files": files,
        "total_files": len(files),
    }
    return manifest

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CDN manifest for a date folder.")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under batches/public-merged/")
    parser.add_argument("--out", default="manifest.json")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if token:
        login(token=token, add_to_git_credential=False)

    manifest = build_manifest(args.repo, args.date)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {args.out} with {manifest['total_files']} files")

if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x bin/generate_manifest.py
```

---

### 2) Python worker (replaces dataset-enrich.sh)

`bin/dataset_enrich.py`

```python
#!/usr/bin/env python3
"""
Robust per-shard enr

## review — reviewer @ 2026-05-03T04:22:42.724422Z

APPROVE: Manifest-driven CDN bypass and Python worker are a clear, workable step forward that directly addresses HF API rate limits and mixed-schema CastErrors; incremental progress with testable acceptance criteria.

Acceptance criteria (downstream tester can check):
- `bin/generate_manifest.py --date YYYY-MM-DD` produces valid `manifest.json` containing `repo`, `date`, `files[]` with `path`, `slug`, `cdn_url`, and non-null `size`/`etag` for every file in `batches/public-merged/{date}/`.
- Training data loader can consume `manifest.json` and fetch every `cdn_url` via HTTP (no HF API calls during data load) and successfully parse each line as JSON with at least `prompt` and `response` fields.
- `bin/dataset_enrich.py --shard-id N --shard-total 16 --date YYYY-MM-DD --manifest manifest.json` emits `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` containing only projected `{prompt,response}` records, with no mixed-schema CastError and bounded memory usage (process streams line-by-line).
- Deduplication via `lib/dedup.py` is exercised and duplicate content (by content hash) is omitted from output shards.
- GitHub Action step (or local run) can generate the manifest and make it available to the 16-shard matrix before workers start, and workers fail fast if manifest is missing or malformed.

## qa — qa @ 2026-05-03T04:22:56.990488Z

PASS: Manifest-driven CDN bypass and Python worker plan is approved.

1) **Acceptance criteria**
- `bin/generate_manifest.py --date YYYY-MM-DD` exits 0 and writes `manifest.json` with top-level keys `repo`, `date`, `folder`, `files[]`; every file entry has non-null `path`, `slug`, `cdn_url`, `size` (int ≥ 0), `etag` (string).
- All `cdn_url` values in `manifest.json` are valid HTTPS URLs pointing to `huggingface.co/datasets/.../resolve/main/...` and contain no Hugging Face Hub API query parameters.
- Training data loader consuming `manifest.json` performs zero Hugging Face Hub API calls (verified by mocking) and successfully parses every line from every fetched CDN file as JSON containing at least `prompt` and `response` string fields.
- `bin/dataset_enrich.py --shard-id N --shard-total 16 --date YYYY-MM-DD --manifest manifest.json` emits `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` where each line is valid JSON with exactly `{prompt, response}`; memory usage stays bounded (streaming line-by-line) and no `CastError` or mixed-schema exception is raised.
- Deduplication via `lib/dedup.py` omits records whose content hash (e.g., SHA-256 of normalized `prompt+response`) has been seen; duplicate rate in output shards is 0%.
- GitHub Action (or local orchestration) generates `manifest.json` and makes it available to all 16 shards before workers start; any worker started without a valid manifest fails fast with a clear error and non-zero exit code.

2) **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_generate_manifest.py
def test_slug_for_path():
    assert slug_for_path("batches/public-merged/2026-05-03/shard0-120000.jsonl") == "shard0-120000"
    assert slug_for_path("batches/public-merged/2026-05-03/shard1.parquet") == "shard1"

def test_build_manifest_structure(mocker):
    mock_items = [
        type("Item", (), {"type": "file", "path": "batches/public-merged/2026-05-03/shard0-120000.jsonl", "size": 1024, "etag": '"abc123"'})(),
    ]
    mocker.patch("huggingface_hub.HfApi.list_repo_tree", return_value=mock_items)
    manifest = build_manifest("axentx/surrogate-1-training-pairs", "2026-05-03")
    assert manifest["repo"] == "axentx/surrogate-1-training-pairs"
    assert manifest["date"] == "2026-05-03"
    assert len(manifest["files"]) == 1
    f = manifest["files"][0]
    assert f["path"] and f["slug"] and f["cdn_url"] and f["size"] is not None and f["etag"]
    assert f["cdn_url"].startswith("https://huggingface.co/datasets/")
    assert "api" not in f["cdn_url"]

# tests/unit/test_dataset_enrich.py
def test_shard_assignment_deterministic():
    from bin.dataset_enrich import assign_to_shard
    slug = "shard0-120000"
    assert assign_to_shard(slug, shard_total=16) == (hash(slug) % 16)

def test_projection_keeps_only_prompt_response():
    from bin.dataset_enrich import project_record
    rec = {"prompt": "hi", "response": "ok", "extra": "x", "meta": {"a": 1}}
    assert project_record(rec) == {"prompt": "hi", "response": "ok"}

def test_streaming_line_by_line_bounds_memory(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data='{"prompt":"a","response":"b"}\n' * 1000))
    from bin.dataset_enrich import stream_file_lines
    count = 0
    for _ in stream_file_lines("fake.jsonl"):
        count += 1
    assert count == 1000

# tests/unit/test_dedup.py
def test_dedup_omits_duplicates():
    from lib.dedup import content_hash, dedup_stream
    rec1 = {"prompt": "x", "response": "y"}
    rec2 = {"prompt": "x", "response": "y"}
    rec3 = {"prompt": "z", "response": "w"}
    items = [rec1, rec2, rec3]
    out = list(dedup_stream(items))
    assert len(out) == 2
    assert content_hash(rec1) == content_hash(rec2)
```

3) **Integration tests** (3 happy + 3 edge)

Happy paths:
- Happy 1 — Manifest generation + CDN fetch: run
