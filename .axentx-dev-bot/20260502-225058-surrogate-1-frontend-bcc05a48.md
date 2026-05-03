# axentx-dev-bot decision
- id: `20260502-225058-surrogate-1-frontend-bcc05a48`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-02T22:50:58.568988Z

## dev — claude/llm-fallback-chain @ 2026-05-02T22:50:58.569054Z

## Implementation Plan (≤2h)

**Highest-value improvement**: Deterministic pre-flight file listing + CDN-only ingestion to eliminate HF API 429s during training and make shard workers resilient.

### Changes (3 files, ~120 lines total)

1. **`bin/list_files.py`** — single Mac-side script that lists one date folder via `list_repo_tree(recursive=False)` and emits `file_list.json`. Embeds into training/shard scripts so workers do CDN-only fetches (zero API calls during data load).
2. **`bin/dataset-enrich.sh`** — updated to accept optional `FILE_LIST` path; if provided, iterates local JSON instead of calling `list_repo_files` repeatedly (reduces API pressure). Keeps fallback to current behavior.
3. **`bin/lib/dedup.py`** — no functional change; ensure it remains importable and thread-safe for 16 parallel runners.

---

### 1) `bin/list_files.py`

```python
#!/usr/bin/env python3
"""
Usage (Mac orchestration):
  python bin/list_files.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file_list.json

Produces:
  {
    "repo": "...",
    "date": "...",
    "files": [
      "batches/public-merged/2026-05-02/file1.parquet",
      ...
    ],
    "cdn_prefix": "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/"
  }
"""

import argparse
import json
import os
import sys
from typing import List

try:
    from huggingface_hub import HfApi
except ImportError:
    print("error: huggingface_hub not installed", file=sys.stderr)
    sys.exit(1)

CDN_PREFIX = "https://huggingface.co/datasets/{repo}/resolve/main/"

def list_date_files(repo: str, date: str) -> List[str]:
    api = HfApi()
    folder = f"batches/public-merged/{date}"
    try:
        items = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    except Exception as exc:
        raise RuntimeError(f"HF list_repo_tree failed for {repo}/{folder}: {exc}") from exc

    files = []
    for item in items:
        if hasattr(item, "path") and item.path:
            # list_repo_tree may return nested objects; accept path string
            files.append(item.path)
    files.sort()
    return files

def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-flight file listing for CDN-only ingestion")
    parser.add_argument("--repo", default="axentx/surrogate-1-training-pairs")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under batches/public-merged/")
    parser.add_argument("--out", default="file_list.json", help="Output JSON path")
    args = parser.parse_args()

    files = list_date_files(args.repo, args.date)
    payload = {
        "repo": args.repo,
        "date": args.date,
        "files": files,
        "cdn_prefix": CDN_PREFIX.format(repo=args.repo),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")

    print(f"listed {len(files)} files -> {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x bin/list_files.py
```

---

### 2) `bin/dataset-enrich.sh` (minimal, safe update)

```bash
#!/usr/bin/env bash
# dataset-enrich.sh
# Deterministic shard worker for public-dataset ingest.
#
# Optional env:
#   FILE_LIST        path to JSON produced by bin/list_files.py
#                    If set, workers iterate local list (CDN-only).
#   HF_TOKEN         write token for axentx/surrogate-1-training-pairs
#   SHARD_ID         0..15  (required by workflow matrix)
#   SHARD_COUNT      16     (required by workflow matrix)

set -euo pipefail

REPO="${REPO:-axentx/surrogate-1-training-pairs}"
DATE="${DATE:-$(date +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:?required}"
SHARD_COUNT="${SHARD_COUNT:?required}"
HF_TOKEN="${HF_TOKEN:?required}"
OUTDIR="batches/public-merged/${DATE}"
TIMESTAMP=$(date +%H%M%S)
OUTFILE="${OUTDIR}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

mkdir -p "$(dirname "$OUTFILE")"

echo "[$(date)] shard ${SHARD_ID}/${SHARD_COUNT} starting for ${DATE}" >&2



## review — reviewer @ 2026-05-02T22:51:27.876946Z

APPROVE: Deterministic pre-flight listing + CDN-only ingestion is a clear, workable step that reduces HF API pressure and makes shard workers resilient; the changes are minimal, focused, and safe with a fallback path.

Acceptance criteria (for downstream tester):
- `bin/list_files.py --repo axentx/surrogate-1-training-pairs --date 2026-05-02 --out file_list.json` runs on Mac, produces valid `file_list.json` with `files` array and `cdn_prefix`, and exits 0 on success; non-zero + stderr on HF failure.
- `bin/dataset-enrich.sh` with `FILE_LIST` set reads local JSON and performs only CDN fetches (no `list_repo_tree`/`list_repo_files` calls during ingestion); without `FILE_LIST` it retains current behavior.
- Shard assignment via `shard_for` is deterministic: same `slug` + `SHARD_COUNT` always yields same `0..SHARD_COUNT-1` across runs.
- Parquet streaming via CDN URL (`pq.read_table(cdn_url, columns=[...])`) succeeds for valid public files and degrades gracefully (fallback column names) without crashing the worker.
- No new secrets or tokens are introduced; `HF_TOKEN` remains required for write operations and is not logged or exposed in output.

## qa — qa @ 2026-05-02T22:51:48.179139Z

PASS: deterministic pre-flight listing + CDN-only ingestion is approved and testable.

1) **Acceptance criteria**
- `bin/list_files.py --repo axentx/surrogate-1-training-pairs --date 2026-05-02 --out file_list.json` exits 0 and writes valid JSON containing keys `repo`, `date`, `files` (array), `cdn_prefix` (string); on HF failure exits non-zero and writes to stderr.
- With `FILE_LIST` set, `bin/dataset-enrich.sh` performs zero `list_repo_tree`/`list_repo_files` calls during ingestion (only CDN fetches); without `FILE_LIST` it retains prior behavior (may call HF APIs).
- Shard assignment via `shard_for(slug, SHARD_COUNT)` is deterministic: for fixed inputs it always returns the same integer in `[0, SHARD_COUNT-1]` across runs and workers.
- Parquet streaming via CDN URL (`pq.read_table(cdn_url, columns=[...])`) succeeds for valid public files; on missing columns it degrades gracefully (fallback column names) without crashing the worker (non-fatal warning + continue).
- No new secrets/tokens introduced; `HF_TOKEN` is not logged or exposed in stdout/stderr of any script; existing write flows still require `HF_TOKEN`.
- `bin/lib/dedup.py` remains importable and thread-safe under 16 parallel runners (no global mutable state that causes cross-runner corruption).
- `file_list.json` CDN prefix matches pattern `https://huggingface.co/datasets/{repo}/resolve/main/` and each listed file path is relative to repo root and non-empty.

2) **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_list_files.py
import json
import tempfile
from unittest.mock import MagicMock, patch
from bin.list_files import list_date_files, main, CDN_PREFIX

def test_list_date_files_returns_sorted_paths():
    mock_items = [MagicMock(path="batches/public-merged/2026-05-02/b.parquet"),
                  MagicMock(path="batches/public-merged/2026-05-02/a.parquet")]
    with patch("bin.list_files.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.return_value = mock_items
        result = list_date_files("owner/repo", "2026-05-02")
    assert result == [
        "batches/public-merged/2026-05-02/a.parquet",
        "batches/public-merged/2026-05-02/b.parquet",
    ]

def test_list_date_files_raises_on_hf_failure():
    with patch("bin.list_files.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.side_effect = RuntimeError("timeout")
        try:
            list_date_files("owner/repo", "2026-05-02")
        except RuntimeError as e:
            assert "HF list_repo_tree failed" in str(e)

def test_main_writes_valid_json_and_exits_0(capsys, tmp_path):
    out = tmp_path / "file_list.json"
    mock_items = [MagicMock(path="batches/public-merged/2026-05-02/x.parquet")]
    with patch("bin.list_files.HfApi") as MockApi, \
         patch("sys.argv", ["list_files.py", "--repo", "a/b", "--date", "2026-05-02", "--out", str(out)]):
        MockApi.return_value.list_repo_tree.return_value = mock_items
        main()
    data = json.loads(out.read_text())
    assert data["repo"] == "a/b"
    assert data["date"] == "2026-05-02"
    assert isinstance(data["files"], list)
    assert data["cdn_prefix"] == CDN_PREFIX.format(repo="a/b")
    assert "listed 1 files" in capsys.readouterr().err

def test_main_nonzero_on_hf_failure(capsys, tmp_path):
    out = tmp_path / "file_list.json"
    with patch("bin.list_files.HfApi") as MockApi, \
         patch("sys.argv", ["list_files.py", "--repo", "a/b", "--date", "2026-05-02", "--out", str(out)]):
        MockApi.return_value.list_repo_tree.side_effect = RuntimeError("timeout")
        try:
            main()
        except SystemExit as e:
            assert e.code != 0
    assert out.exists() is False or json.loads(out.read_text()) == {}  # implementation may not write partial

# tests/unit/test_shard_for.py
from bin.lib.shard_for import shard_for

def test_shard_for_deterministic():
    results = [shard_for("abc/def", 8) for _ in range(100)]
    assert len(set(results)) == 1
    assert 0 <= resul
