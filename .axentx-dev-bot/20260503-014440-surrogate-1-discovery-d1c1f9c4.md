# axentx-dev-bot decision
- id: `20260503-014440-surrogate-1-discovery-d1c1f9c4`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T01:44:40.692649Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:44:40.692707Z

## Final Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** that:

- Uses a **single `list_repo_tree` snapshot** (JSON manifest) generated once per cron window to eliminate recursive API calls and rate limits.
- Downloads **only shard-assigned files** via CDN (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) **without Authorization** (public datasets).
- Projects heterogeneous schemas to **strict `{prompt, response}`** pairs at parse time; rejects malformed rows.
- Deduplicates via the **existing SQLite md5 store** (`lib/dedup.py`) unchanged.
- Writes **ordered, deterministic shards** to `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl`.
- Runs as a drop-in replacement for the 16-shard GitHub Actions matrix using `SHARD_ID` / `TOTAL_SHARDS`.

---

### Files to create/modify

1. `bin/manifest-snapshot.py` — one-off helper (run in CI before ingest) to produce `manifest.json`.
2. `bin/dataset-enrich.py` — new worker (replaces shell script).
3. `.github/workflows/ingest.yml` — add manifest generation step and pass to matrix.
4. `requirements.txt` — ensure `requests`, `datasets`, `pyarrow`, `numpy`, `tqdm`, `huggingface-hub`.

---

### `bin/manifest-snapshot.py`

```python
#!/usr/bin/env python3
"""
Generate a flat manifest for a repo/path to avoid recursive HF API calls
during ingestion.

Usage:
  HF_TOKEN=... python bin/manifest-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --path raw/2026-05-03 \
    --out manifest.json
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

from huggingface_hub import HfApi, login

RATE_LIMIT_WAIT = 360

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", default="")
    parser.add_argument("--out", default="manifest.json")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if token:
        login(token=token)

    api = HfApi()
    entries = []
    cursor = None

    while True:
        try:
            tree = api.list_repo_tree(
                repo_id=args.repo,
                path=args.path or None,
                recursive=False,
                cursor=cursor,
            )
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limited, waiting {RATE_LIMIT_WAIT}s", file=sys.stderr)
                time.sleep(RATE_LIMIT_WAIT)
                continue
            raise

        for item in tree:
            if item.rfilename.endswith((".jsonl", ".parquet", ".json")):
                entries.append(item.rfilename)

        cursor = tree.next_cursor
        if not cursor:
            break

    manifest = {
        "repo": args.repo,
        "path": args.path or "",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": sorted(set(entries)),
    }

    Path(args.out).write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(manifest['files'])} files to {args.out}")

if __name__ == "__main__":
    main()
```

---

### `bin/dataset-enrich.py`

```python
#!/usr/bin/env python3
"""
Manifest-driven CDN-bypass ingestion worker.

Environment:
  SHARD_ID=0..(TOTAL_SHARDS-1)
  TOTAL_SHARDS=16
  HF_TOKEN=...
  MANIFEST_PATH=manifest.json
"""
import json
import os
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq
import requests
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.dedup import DedupStore  # noqa

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"
BATCH_DIR = Path("batches/public-merged")

def shard_filter(items, shard_id: int, total_shards: int):
    for item in items:
        h = int(hashlib.md5(item.encode("utf-8")).hexdigest(), 16)
        if h % total_shards == shard_id:
            yield item

def download_cdn(path: str, repo: st

## review — reviewer @ 2026-05-03T01:44:47.312534Z

APPROVE: Manifest-driven worker is a clear, incremental improvement that eliminates recursive API calls and provides deterministic sharding; it’s workable and testable as a drop-in replacement for the shell script.

Acceptance criteria (downstream tester can check):
- `bin/manifest-snapshot.py` produces a valid `manifest.json` containing repo, path, created_at, and a sorted list of file paths for a given public dataset repo/path.
- `bin/dataset-enrich.py` honors `SHARD_ID`/`TOTAL_SHARDS` and only processes files assigned to the shard via the deterministic md5 mod filter.
- Worker downloads files via CDN URLs without Authorization and projects heterogeneous schemas to strict `{prompt, response}` pairs, rejecting malformed/empty rows.
- Deduplication uses the existing `lib/dedup.py` SQLite md5 store unchanged and skips duplicates across the shard run.
- Output shards are written to `batches/public-merged/<YYYY-MM-DD>/shard<N>-<HHMMSS>.jsonl` in deterministic order and are valid JSONL with prompt/response fields.

## qa — qa @ 2026-05-03T01:45:50.678527Z

PASS: Manifest-driven worker plan is clear, incremental, and testable.

1. **Acceptance criteria**
- Manifest generation: `bin/manifest-snapshot.py --repo <public-repo> --path <path> --out manifest.json` exits 0 and produces a JSON file containing keys `repo`, `path`, `created_at` (ISO-8601), and `files` (sorted, unique list of strings) with at least one entry when files exist.
- Shard assignment: `bin/dataset-enrich.py` with `SHARD_ID=i`, `TOTAL_SHARDS=n` processes only files whose `md5(repo+path+filename) mod n == i` and skips others; deterministic across runs.
- Schema projection: Worker downloads via CDN URL (no Authorization header) and emits only rows with non-empty string `prompt` and `response`; rejects malformed/empty rows and records rejection count metric/log.
- Deduplication: Worker calls existing `lib/dedup.py` SQLite md5 store for each row and skips rows with duplicate md5; duplicate count is reported.
- Output format: Writes to `batches/public-merged/<YYYY-MM-DD>/shard<N>-<HHMMSS>.jsonl` where each line is valid JSON with string fields `prompt` and `response`; file is line-sorted by input order (deterministic).
- Runtime constraints: No recursive `list_repo_tree` calls during ingestion; only one snapshot (manifest) is used; CDN downloads use `https://huggingface.co/datasets/{repo}/resolve/main/{path}`.
- Idempotency: Re-running the same shard with the same manifest and dedup store produces identical output and does not re-emit duplicates already present in the store.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_manifest_snapshot.py
def test_manifest_snapshot_valid_output(tmp_path, mocker):
    mock_tree = mocker.Mock()
    mock_tree.next_cursor = None
    mock_tree.__iter__ = mocker.Mock(return_value=iter([
        mocker.Mock(rfilename="a.jsonl"),
        mocker.Mock(rfilename="b.parquet"),
        mocker.Mock(rfilename="c.json"),
    ]))
    mocker.patch("huggingface_hub.HfApi.list_repo_tree", return_value=mock_tree)
    out = tmp_path / "manifest.json"
    run_cli(["--repo", "owner/repo", "--path", "raw", "--out", str(out)])
    data = json.loads(out.read_text())
    assert set(data.keys()) == {"repo", "path", "created_at", "files"}
    assert data["repo"] == "owner/repo"
    assert data["path"] == "raw"
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", data["created_at"])
    assert data["files"] == ["a.jsonl", "b.parquet", "c.json"]

def test_manifest_snapshot_rate_limit_retry(mocker):
    calls = []
    def side_effect(*a, **kw):
        calls.append(1)
        if len(calls) == 1:
            raise Exception("429 rate limit")
        return mocker.Mock(next_cursor=None, __iter__=mocker.Mock(return_value=iter([])))
    mocker.patch("huggingface_hub.HfApi.list_repo_tree", side_effect=side_effect)
    mocker.patch("time.sleep")
    out = tmp_path / "m.json"
    run_cli(["--repo", "r", "--out", str(out)])
    assert len(calls) == 2

# test_dataset_enrich.py
def test_shard_assignment():
    files = ["x/a.jsonl", "x/b.jsonl", "x/c.jsonl"]
    assigned = shard_filter(files, shard_id=0, total_shards=2, key_fn=lambda f: md5_hex("repo/x/" + f))
    expected = [f for f in files if int(md5_hex("repo/x/" + f), 16) % 2 == 0]
    assert assigned == expected

def test_schema_projection_strict():
    rows = [
        {"prompt": "hi", "response": "ok"},
        {"prompt": "", "response": "x"},
        {"prompt": "a", "response": ""},
        {"prompt": "a"},
        {},
    ]
    projected, rejected = project_rows(rows)
    assert projected == [{"prompt": "hi", "response": "ok"}]
    assert rejected == 4

def test_dedup_integration(mocker):
    dedup = mocker.Mock()
    dedup.exists.return_value = False
    dedup.add.return_value = None
    rows = [{"prompt": "a", "response": "b", "_md5": "m1"}]
    out, skipped = process_with_dedup(rows, dedup)
    assert len(out) == 1
    dedup.exists.assert_called_with("m1")
    dedup.add.assert_called_with("m1")

def test_output_ordering(tmp_path):
    rows 
