# axentx-dev-bot decision
- id: `20260502-190547-surrogate-1-discovery-0926aa1b`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T19:05:47.737028Z

## dev — claude/llm-fallback-chain @ 2026-05-02T19:05:47.737089Z

## Final Implementation Plan (≤2h)

**Goal:** deterministic ingestion, CDN-bypass, API-efficient, idempotent, and race-safe.

### Core decisions (resolve contradictions)
- Use **UTC date partition** `batches/public-merged/{YYYY-MM-DD}/` (both candidates agree).
- **Single pre-flight `list_repo_tree` call** per run (non-recursive) to produce `file-list.json`; embed it so workers never list during training (reduces API pressure and enables CDN-only fetches).
- **Shard assignment unchanged** (`slug-hash % 16`) but operate only on files from the pre-fetched list (deterministic and rate-limit safe).
- **Idempotent filenames** include `HHMMSS` in the worker output filename; skip upload if target exists (fast-fail/continue).
- **CDN-bypass download** via raw `https://huggingface.co/datasets/.../resolve/main/...` (no auth header) using the pre-computed list.
- **HF_TOKEN used only for upload**, not for listing during training.
- **Local test** with a mock list to verify paths and CDN URLs resolve.

---

### 1) New script: `bin/build-file-list.sh` (pre-flight generator)

```bash
#!/usr/bin/env bash
set -euo pipefail
# Usage: RUN_DATE=YYYY-MM-DD ./bin/build-file-list.sh
# Produces: file-list.json  (JSON object with date + files array)

: "${HF_TOKEN:?}"
: "${RUN_DATE:=$(date -u +%Y-%m-%d)}"

REPO="datasets/axentx/surrogate-1-training-pairs"

python -c "
import json, os, datetime, sys
from huggingface_hub import HfApi
api = HfApi(token=os.getenv('HF_TOKEN'))
repo = 'datasets/axentx/surrogate-1-training-pairs'
today = os.getenv('RUN_DATE', datetime.datetime.utcnow().strftime('%Y-%m-%d'))
files = [f.rfilename for f in api.list_repo_tree(repo, path=today, recursive=False)]
out = {'date': today, 'files': sorted(files)}
with open('file-list.json', 'w') as f:
    json.dump(out, f, indent=2)
print(json.dumps(out))
"
```

---

### 2) Updated workflow: `.github/workflows/ingest.yml`

```yaml
name: ingest
on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  file-list:
    runs-on: ubuntu-latest
    outputs:
      date: ${{ steps.vars.outputs.date }}
      file_list: ${{ steps.list.outputs.files }}
    steps:
      - uses: actions/checkout@v4
      - name: Install deps
        run: pip install huggingface_hub
      - name: Generate file list (single API call)
        id: list
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
          RUN_DATE: ""  # let script default to UTC today
        run: |
          bash bin/build-file-list.sh
          echo "files=$(jq -c .files file-list.json)" >> $GITHUB_OUTPUT
          echo "date=$(jq -r .date file-list.json)" >> $GITHUB_OUTPUT
      - name: Upload file-list artifact
        uses: actions/upload-artifact@v4
        with:
          name: file-list
          path: file-list.json

  ingest-shard:
    needs: file-list
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard_id: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    steps:
      - uses: actions/checkout@v4
      - name: Download file-list
        uses: actions/download-artifact@v4
        with:
          name: file-list
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run shard worker
        env:
          SHARD_ID: ${{ matrix.shard_id }}
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
          FILE_LIST: file-list.json
          RUN_DATE: ${{ needs.file-list.outputs.date }}
        run: |
          bash bin/dataset-enrich.sh
```

---

### 3) Updated worker: `bin/dataset-enrich.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# Required env
: "${SHARD_ID:?}"
: "${HF_TOKEN:?}"
: "${RUN_DATE:?}"
: "${FILE_LIST:?}"

REPO="datasets/axentx/surrogate-1-training-pairs"
OUT_DIR="output"
mkdir -p "$OUT_DIR"

# Parse file list (JSON array of filenames)
if [[ -f "$FILE_LIST" ]]; then
  mapfile -t FILES < <(jq -r '.files[]' "$FILE_LIST")
else
  echo "No file list provided at $FILE_LIST" >&2
  exit 1
fi

# Deterministic output path (idempotent)
TS=$(date -u +"%H%M%S")
OUT_PATH="${OUT_DIR}/

## review — reviewer @ 2026-05-02T19:06:02.567826Z

APPROVE: proposes a coherent, incremental plan that addresses determinism, CDN-bypass, idempotency, and race-safety with concrete artifacts and acceptance criteria a tester can validate.

Acceptance criteria:
- `bin/build-file-list.sh` produces valid `file-list.json` with `{date, files[]}` and exits non-zero on HF_TOKEN missing or list failure.
- Workflow `file-list` job outputs `date` and `files` and uploads `file-list.json` artifact; `ingest-shard` jobs download it and run without listing the repo tree again.
- Worker `bin/dataset-enrich.sh` uses only the provided `FILE_LIST`, assigns shards via `slug-hash % 16`, and skips files not assigned to `SHARD_ID`.
- Downloads use the CDN URL pattern `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{file}` with no auth header; HF_TOKEN is used only for upload.
- Output filenames include `HHMMSS` and upload step is idempotent (skip if target exists); overall run is deterministic given the same `RUN_DATE` and `file-list.json`.

## qa — qa @ 2026-05-02T19:06:36.795416Z

PASS

1. **Acceptance criteria**
- `bin/build-file-list.sh` exits 0 and emits valid `file-list.json` with required schema `{date:YYYY-MM-DD, files:[non-empty strings]}` when `HF_TOKEN` is present and list succeeds; exits non-zero and emits nothing on missing `HF_TOKEN` or list failure.
- Workflow `file-list` job outputs `date` (YYYY-MM-DD) and `files` (JSON array) and uploads `file-list.json` artifact; `ingest-shard` jobs download the artifact and complete without calling `list_repo_tree` (verified by absence of list calls in logs).
- Worker `bin/dataset-enrich.sh` consumes `FILE_LIST` path, assigns shards by `slug-hash % 16`, and processes only files assigned to `SHARD_ID` (0–15); rejects or skips unassigned files.
- Downloads use CDN URL pattern `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/{file}` with no `Authorization` header; `HF_TOKEN` is used only during upload (verified by header presence/absence per request).
- Output filenames embed `HHMMSS` (UTC) in the basename (e.g., `{prefix}-{slug}-{HHMMSS}.parquet`); upload step is idempotent: skips when target exists and returns success without re-upload.
- Given identical `RUN_DATE` and `file-list.json`, shard assignment and produced filenames are deterministic across runs (same inputs → same outputs).
- Script handles missing/empty `file-list.json` gracefully (non-zero exit and clear error) and does not proceed to download/process steps.

2. **Unit tests** (pytest-style pseudo-code)

```python
# test_build_file_list.py
import json, os, subprocess, tempfile, pytest
from unittest import mock

def test_build_file_list_success():
    with mock.patch.dict(os.environ, {"HF_TOKEN": "x", "RUN_DATE": "2025-01-01"}):
        with mock.patch("huggingface_hub.HfApi.list_repo_tree") as m:
            m.return_value = [type("Obj", (), {"rfilename": "2025-01-01/a.json"})()]
            out = subprocess.check_output(["bash", "bin/build-file-list.sh"], text=True)
            data = json.loads(out)
            assert data["date"] == "2025-01-01"
            assert data["files"] == ["2025-01-01/a.json"]
            assert os.path.exists("file-list.json")

def test_build_file_list_missing_token():
    with mock.patch.dict(os.environ, {}, clear=True):
        result = subprocess.run(["bash", "bin/build-file-list.sh"], capture_output=True)
        assert result.returncode != 0

# test_dataset_enrich.py
import hashlib, json, tempfile, os
from dataset_enrich import assign_shard, build_cdn_url, should_process

def slug_hash(s):
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)

def test_assign_shard():
    for slug in ["abc", "xyz", "foo/bar"]:
        assert 0 <= assign_shard(slug) <= 15
        assert assign_shard(slug) == slug_hash(slug) % 16

def test_build_cdn_url():
    assert build_cdn_url("2025-01-01/a.json") == \
        "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/2025-01-01/a.json"

def test_should_process():
    slug = "item-123"
    shard = assign_shard(slug)
    assert should_process(slug, shard, list(range(16))) is True
    assert should_process(slug, (shard + 1) % 16, list(range(16))) is False

def test_skip_unassigned():
    files = ["2025-01-01/a.json", "2025-01-01/b.json"]
    assignments = {f: assign_shard(f) for f in files}
    for shard_id in range(16):
        selected = [f for f in files if assign_shard(f) == shard_id]
        # simulate worker behavior
        assert all(assign_shard(f) == shard_id for f in selected)
```

3. **Integration tests**

Happy paths (3)
- End-to-end dry-run with mock `file-list.json` (two files) and `SHARD_ID=3`: worker downloads via CDN URLs (no auth), produces UTC-HHMMSS filenames, and skips upload (mock upload endpoint returns 200 for idempotent skip). Verify no repo-tree API calls occur after file-list generation.
- Full workflow simulation (local act or GH Actions dry-run): `file-list` job emits artifact; two matrix `ingest-shard` jobs consume it and produce disjoin
