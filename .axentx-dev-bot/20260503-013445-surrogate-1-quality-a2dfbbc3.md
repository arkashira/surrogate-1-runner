# axentx-dev-bot decision
- id: `20260503-013445-surrogate-1-quality-a2dfbbc3`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-03T01:34:45.591332Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:34:45.591413Z

### Final Implementation Plan (≤2h)

**Goal**: Eliminate HF API rate-limit risk and OOM in the surrogate-1 ingestion pipeline by replacing recursive authenticated fetches with deterministic shard routing + CDN-only fetches.

---

#### 1) `bin/dataset-enrich.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# Usage: dataset-enrich.sh <date> <shard_id> <total_shards>
# Example: dataset-enrich.sh 2026-05-03 0 16

DATE="${1:-$(date +%Y-%m-%d)}"
SHARD_ID="${2:-${SHARD_ID:-0}}"
TOTAL_SHARDS="${3:-${TOTAL_SHARDS:-16}}"
HF_REPO="${HF_REPO:-datasets/axentx/surrogate-1-training-pairs}"
HF_TOKEN="${HF_TOKEN:?HF_TOKEN required}"
OUT_DIR="batches/public-merged/${DATE}"
TIMESTAMP=$(date +%H%M%S)
OUTPUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${TIMESTAMP}.jsonl"

mkdir -p "$(dirname "${OUTPUT_FILE}")"

echo "[$(date)] Shard ${SHARD_ID}/${TOTAL_SHARDS} | Date ${DATE}"
echo "Listing ${HF_REPO} tree for ${DATE}..."

# Single non-recursive tree call per date folder (avoids recursive pagination)
TREE_JSON=$(python3 -c "
import json, os, sys
from huggingface_hub import HfApi
api = HfApi(token=os.environ['HF_TOKEN'])
items = api.list_repo_tree(
    repo_id=os.environ['HF_REPO'],
    path='${DATE}',
    repo_type='dataset',
    recursive=False
)
# Keep only files (ignore subfolders)
files = [i for i in items if i.type == 'file']
print(json.dumps([f.rfilename for f in files]))
" 2>/dev/null || python3 -c "
# Fallback: if HF SDK not available, use raw API (still one call)
import json, os, sys, urllib.request
token = os.environ['HF_TOKEN']
url = f'https://huggingface.co/api/datasets/{os.environ[\"HF_REPO\"]}/tree?path=${DATE}&recursive=false'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req) as resp:
    items = json.load(resp)
files = [i['path'] for i in items if i['type'] == 'file' and i['path'].startswith('${DATE}/')]
print(json.dumps(files))
")

# Deterministic shard assignment by slug hash
FILTERED=$(python3 -c "
import json, hashlib, sys
files = json.loads(sys.stdin.read())
shard_id = int(${SHARD_ID})
total = int(${TOTAL_SHARDS})
selected = []
for f in files:
    # Use filename as slug; deterministic modulo shard
    slug = f.split('/')[-1]
    h = int(hashlib.sha256(slug.encode()).hexdigest(), 16)
    if (h % total) == shard_id:
        selected.append(f)
print(json.dumps(selected))
" <<< "${TREE_JSON}")

echo "Selected $(echo "${FILTERED}" | python3 -c "import sys,json;print(len(json.load(sys.stdin)))") files for shard ${SHARD_ID}"

# Emit CDN-only URL list for downstream loader (zero API calls during fetch)
python3 -c "
import json, sys, os
files = json.loads(sys.stdin.read())
repo = os.environ['HF_REPO']
urls = [f'https://huggingface.co/datasets/{repo}/resolve/main/{f}' for f in files]
with open('${OUT_DIR}/shard${SHARD_ID}-urls.json', 'w') as f:
    json.dump(urls, f)
" <<< "${FILTERED}"

# Stream selected files via CDN and normalize to {prompt,response}
python3 bin/process_shard.py \
  --urls-file "${OUT_DIR}/shard${SHARD_ID}-urls.json" \
  --output "${OUTPUT_FILE}" \
  --dedup-db "lib/dedup.sqlite"

echo "Writing ${OUTPUT_FILE}"
echo "Uploading to HF dataset..."

git config user.name "github-actions"
git config user.email "actions@github.com"
git add "${OUTPUT_FILE}" "${OUT_DIR}/shard${SHARD_ID}-urls.json" || true
git commit -m "shard${SHARD_ID} ${DATE} ${TIMESTAMP}" || true
git push origin HEAD

echo "[$(date)] Shard ${SHARD_ID} done"
```

---

#### 2) `bin/process_shard.py`

```python
#!/usr/bin/env python3
"""
CDN-only shard processor.
- Reads list of CDN URLs (public dataset files).
- Downloads each file individually via CDN (no auth, no API rate-limit).
- Projects to {prompt,response} and normalizes per known schema.
- Dedups via central SQLite store.
- Outputs newline JSONL.
"""
import argparse
import json
import hashlib
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

import numpy as np
import pyarrow as pa
import pyarrow.parqu

## review — reviewer @ 2026-05-03T01:36:12.460231Z

APPROVE: The change is a workable, incremental step that directly addresses the stated risks (HF API rate-limit and OOM) by replacing recursive authenticated fetches with deterministic shard routing and CDN-only fetches. It provides a clear, testable ingestion path and a fallback mechanism; downstream tests can verify shard assignment, CDN fetch, normalization, and dedup behavior.

Acceptance criteria (downstream tester can check):
- `dataset-enrich.sh` with a given date/shard/total produces deterministic shard assignment (same inputs → same file list) and emits `shard{SHARD_ID}-urls.json` containing only CDN URLs (no `?token=` or API endpoints).
- No authenticated HF API calls occur during file fetch (only the single non-recursive tree call per date); verify by monitoring network traffic or checking that `HF_TOKEN` is not used in download requests.
- `process_shard.py` downloads each CDN URL, normalizes records to `{prompt, response}` (non-empty strings), and writes valid JSONL lines; schema variants (instruction/input/output/question/answer) map correctly.
- Deduplication via `lib/dedup.sqlite` prevents duplicate content (by hash) across runs; reprocessing the same shard does not increase row count for identical content.
- End-to-end run for a small sample date completes without OOM (memory usage stays bounded) and produces at least one output JSONL file in `batches/public-merged/<date>/`.

## qa — qa @ 2026-05-03T01:36:58.463659Z

PASS: Implementation plan approved.

1) **Acceptance criteria**
- Deterministic shard assignment: for fixed (date, shard_id, total_shards, repo tree), `dataset-enrich.sh` emits identical `shard{SHARD_ID}-urls.json` across runs (byte-for-byte URL list).
- CDN-only fetch URLs: every URL in `shard{SHARD_ID}-urls.json` matches pattern `https://huggingface.co/datasets/*/resolve/main/*` and contains no `?token=` or `api.huggingface.co` endpoints.
- No authenticated fetch during download: network trace or HTTP request inspection shows zero requests carrying `Authorization: Bearer` to `huggingface.co` during file download phase (only the single tree call may carry token).
- Normalized JSONL schema: each output line is valid JSON with non-empty string fields `prompt` and `response`; schema variants (`instruction/input/output/question/answer`) map correctly into `prompt`/`response`.
- Deduplication invariant: after processing a shard, reprocessing the same shard does not increase row count in `lib/dedup.sqlite` for content hashes already present.
- Bounded memory / no OOM: peak resident memory during processing stays below 1.5 GB for a shard of up to 500 files (sample size) and does not grow unbounded with file count.
- End-to-end artifact: run completes with exit code 0 and produces at least one file matching `batches/public-merged/<date>/shard{SHARD_ID}-*.jsonl` containing ≥1 valid JSONL line.

2) **Unit tests** (pytest-style pseudo-code)

```python
# test_shard_assignment.py
def test_shard_assignment_deterministic():
    files = [f"2026-05-03/file{i}.jsonl" for i in range(100)]
    selected = shard_select(files, shard_id=3, total_shards=16)
    selected_again = shard_select(files, shard_id=3, total_shards=16)
    assert selected == selected_again

def test_shard_assignment_exhaustive():
    files = [f"2026-05-03/file{i}.jsonl" for i in range(1000)]
    total = 16
    all_selected = []
    for s in range(total):
        all_selected.extend(shard_select(files, shard_id=s, total_shards=total))
    assert sorted(all_selected) == sorted(files)

# test_urls.py
def test_urls_are_cdn_only():
    urls = build_cdn_urls(["2026-05-03/a.jsonl", "2026-05-03/b.jsonl"], repo="datasets/axentx/surrogate-1-training-pairs")
    for u in urls:
        assert u.startswith("https://huggingface.co/datasets/")
        assert "/resolve/main/" in u
        assert "token" not in u
        assert "api.huggingface.co" not in u

# test_normalizer.py
def test_normalize_variant_instruction():
    raw = {"instruction": "Q", "input": "context", "output": "A"}
    out = normalize_record(raw)
    assert out["prompt"] == "Q\ncontext"
    assert out["response"] == "A"

def test_normalize_variant_question():
    raw = {"question": "Q", "answer": "A"}
    out = normalize_record(raw)
    assert out["prompt"] == "Q"
    assert out["response"] == "A"

def test_normalize_rejects_empty():
    raw = {"prompt": "", "response": "ok"}
    assert normalize_record(raw) is None
    raw = {"prompt": "ok", "response": ""}
    assert normalize_record(raw) is None

# test_dedup.py
def test_dedup_insert_new():
    db = DedupDB(":memory:")
    h = "sha256:abc"
    assert db.insert_if_new(h) is True
    assert db.insert_if_new(h) is False
```

3) **Integration tests** (3 happy + 3 edge)

Happy paths:
- IT1 — Single shard, small date: run `dataset-enrich.sh 2026-05-03 0 4` against a fixture repo stub; verify `shard0-urls.json` contains expected CDN URLs, `process_shard.py` downloads and normalizes to JSONL, and `lib/dedup.sqlite` records inserted hashes.
- IT2 — Multi-shard deterministic split: run with total_shards=4 across shard_ids 0-3; confirm union of shard file lists equals full date file set and no overlap.
- IT3 — End-to-end bounded memory: process a shard of 500 fixture files while monitoring RSS; assert peak RSS < 1.5 GB and final artifact exists with ≥1 JSONL line.

Edge cases:
- ET1 — Empty date folder: tree returns no files; script emits empty `shard0-urls.json`, zero downloads, a
