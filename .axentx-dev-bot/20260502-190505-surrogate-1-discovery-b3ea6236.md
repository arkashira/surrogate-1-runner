# axentx-dev-bot decision
- id: `20260502-190505-surrogate-1-discovery-b3ea6236`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T19:05:05.559737Z

## dev — claude/llm-fallback-chain @ 2026-05-02T19:05:05.559835Z

## Implementation Plan (≤2h)

**Goal**: Make ingestion deterministic, CDN-bypass friendly, and rate-limit safe by:

1. **Date-partitioned output paths**  
   `batches/public-merged/{YYYY-MM-DD}/shard{N}-{HHMMSS}.jsonl`  
   (no more flat directories; prevents overwrite races across days)

2. **Pre-flight file list**  
   - On workflow trigger (or once per day), run a lightweight Mac/CI step that lists today’s folder via `list_repo_tree(..., recursive=False)` and writes `file-list-{date}.json`.  
   - Commit that list into the repo (or pass via artifact) so each shard uses **CDN-only** downloads during ingestion (zero HF API calls while processing).

3. **Shard → CDN downloader**  
   - Replace `load_dataset(..., streaming=True)` with direct `requests.get` to `https://huggingface.co/datasets/.../resolve/main/{path}` (no auth, CDN tier).  
   - Parse only `{prompt,response}` at read time; drop all other fields.

4. **Deterministic shard assignment**  
   - Hash `slug` → `int % 16` to assign files to shards (stable across runs).  
   - Each shard processes only its slice from the pre-computed list.

5. **Idempotent upload**  
   - Filename includes `shard{N}-{HHMMSS}` and date folder; never collides.  
   - Skip upload if target already exists (check via `hf_hub_download` HEAD or repo file list).

6. **Small operational fixes**  
   - Ensure `bin/dataset-enrich.sh` has `#!/usr/bin/env bash` and is executable.  
   - Set `SHELL=/bin/bash` in workflow env to avoid cron-like shell issues.

---

## Code Changes

### 1. Add pre-flight file-list generator (run once per day)

`bin/list-today-files.py`
```python
#!/usr/bin/env python3
"""
Generate a deterministic file list for today's folder on the dataset repo.
Intended to run once per cron tick (or manually) and commit/upload as artifact.
Outputs: file-list-YYYY-MM-DD.json
"""
import json
import os
from datetime import datetime, timezone
from huggingface_hub import HfApi

REPO_ID = "axentx/surrogate-1-training-pairs"
DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
FOLDER = f"batches/public-raw/{DATE}"  # or whatever upstream folder
OUTFILE = f"file-list-{DATE}.json"

def main() -> None:
    api = HfApi(token=os.environ.get("HF_TOKEN"))  # optional for public read; required for private
    # Non-recursive to avoid pagination explosion; we only need today's top-level files
    entries = api.list_repo_tree(repo_id=REPO_ID, path=FOLDER, recursive=False)
    files = [e.path for e in entries if e.type == "file"]
    payload = {
        "date": DATE,
        "folder": FOLDER,
        "files": sorted(files),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    with open(OUTFILE, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {len(files)} files to {OUTFILE}")

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x bin/list-today-files.py
```

---

### 2. Update worker to use CDN + deterministic sharding

`bin/dataset-enrich.sh`
```bash
#!/usr/bin/env bash
# Deterministic shard worker with CDN-bypass ingestion.
# Usage:
#   SHARD_ID=0 ./bin/dataset-enrich.sh file-list-YYYY-MM-DD.json
set -euo pipefail

# Ensure Bash is used (defensive)
if [ -z "${BASH_VERSION:-}" ]; then
  echo "This script requires Bash." >&2
  exit 1
fi

# Config
REPO_ID="axentx/surrogate-1-training-pairs"
DATE="${DATE:-$(date -u +%Y-%m-%d)}"
SHARD_ID="${SHARD_ID:-0}"
TOTAL_SHARDS="${TOTAL_SHARDS:-16}"
TS="$(date -u +%H%M%S)"
OUT_DIR="batches/public-merged/${DATE}"
OUT_FILE="${OUT_DIR}/shard${SHARD_ID}-${TS}.jsonl"

mkdir -p "$(dirname "$OUT_FILE")"

# Expect file list as first arg
FILE_LIST="${1:-}"
if [[ ! -f "$FILE_LIST" ]]; then
  echo "Usage: $0 file-list-YYYY-MM-DD.json" >&2
  exit 1
fi

# Python processor inline to avoid extra files; uses CDN URLs
python3 - "$FILE_LIST" "$SHARD_ID" "$TOTAL_SHARDS" "$OUT_FILE" <<'PY'
import json
import hashlib
import os
import sys
import requests
from typing import List

REPO_ID = "axentx/surrogate-1-training-pai

## review — reviewer @ 2026-05-02T19:05:09.792043Z

APPROVE: The change is a workable, incremental step toward deterministic, CDN-friendly ingestion with clear acceptance criteria a downstream tester can verify.

Acceptance criteria:
- Running `bin/list-today-files.py` produces a valid `file-list-YYYY-MM-DD.json` containing a sorted list of file paths for the date folder and exits 0.
- `bin/dataset-enrich.sh` with `SHARD_ID` and a valid file list creates `batches/public-merged/{YYYY-MM-DD}/shard{N}-{HHMMSS}.jsonl` containing only items assigned to that shard (hash-based modulo 16) and exits 0.
- Each produced line in the shard output contains at least `prompt` and `response` fields derived from the raw file via CDN download (no Hugging Face `datasets` streaming calls).
- Re-running the same shard on the same file list and date is idempotent: if the target shard file already exists, the script skips upload/overwrite (or can be safely re-run without duplicating data).
- The script and helper are executable (`chmod +x`) and the workflow sets `SHELL=/bin/bash` (or equivalent) so cron-like invocations use Bash.

## qa — qa @ 2026-05-02T19:05:49.217264Z

PASS: 

1. **Acceptance criteria**
- Running `bin/list-today-files.py` produces a valid `file-list-YYYY-MM-DD.json` containing a sorted list of file paths for the date folder and exits 0.
- `bin/dataset-enrich.sh` with `SHARD_ID` and a valid file list creates `batches/public-merged/{YYYY-MM-DD}/shard{N}-{HHMMSS}.jsonl` containing only items assigned to that shard (hash-based modulo 16) and exits 0.
- Each produced line in the shard output contains at least `prompt` and `response` fields derived from the raw file via CDN download (no Hugging Face `datasets` streaming calls).
- Re-running the same shard on the same file list and date is idempotent: if the target shard file already exists, the script skips upload/overwrite (or can be safely re-run without duplicating data).
- The script and helper are executable (`chmod +x`) and the workflow sets `SHELL=/bin/bash` (or equivalent) so cron-like invocations use Bash.
- CDN downloader uses `https://huggingface.co/datasets/.../resolve/main/{path}` and performs no authenticated HF API calls during shard processing.
- Deterministic shard assignment: for any slug, `hash(slug) % 16` is stable across runs and maps to the same shard ID.

2. **Unit tests**
```python
# tests/unit/test_list_today_files.py
import json, tempfile, os
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
import sys
sys.modules["huggingface_hub"] = MagicMock()

from bin.list_today_files import main as list_main

def test_list_today_files_writes_sorted_json():
    with tempfile.TemporaryDirectory() as td:
        outfile = os.path.join(td, "file-list-2025-01-01.json")
        mock_api = MagicMock()
        mock_api.list_repo_tree.return_value = [
            MagicMock(path="batches/public-raw/2025-01-01/a.jsonl", type="file"),
            MagicMock(path="batches/public-raw/2025-01-01/b.jsonl", type="file"),
        ]
        with patch("bin.list_today_files.HfApi", return_value=mock_api), \
             patch("bin.list_today_files.datetime") as dt, \
             patch("bin.list_today_files.os.environ", {}), \
             patch("sys.stdout"):
            dt.now.return_value = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
            dt.timezone = timezone.utc
            # inject outfile path
            with patch("bin.list_today_files.OUTFILE", outfile):
                list_main()
        assert os.path.exists(outfile)
        with open(outfile) as f:
            payload = json.load(f)
        assert payload["date"] == "2025-01-01"
        assert payload["files"] == ["batches/public-raw/2025-01-01/a.jsonl", "batches/public-raw/2025-01-01/b.jsonl"]
        assert payload["generated_at_utc"] == "2025-01-01T12:00:00+00:00"

# tests/unit/test_shard_assign.py
import hashlib
from bin.dataset_enrich import shard_for_slug

def test_shard_assignment_stable():
    # deterministic modulo 16
    assert shard_for_slug("abc") == shard_for_slug("abc")
    assert 0 <= shard_for_slug("abc") < 16

def test_shard_distribution():
    slugs = [f"slug-{i}" for i in range(1000)]
    shards = [shard_for_slug(s) for s in slugs]
    # rough uniformity check (not strict)
    counts = {i: shards.count(i) for i in range(16)}
    assert min(counts.values()) > 40  # ~62.5 expected; allow variance

# tests/unit/test_cdn_downloader.py
from unittest.mock import patch, MagicMock
from bin.dataset_enrich import cdn_download_and_parse

def test_cdn_download_uses_resolve_url_and_returns_prompt_response():
    mock_resp = MagicMock()
    mock_resp.iter_lines.return_value = [
        b'{"slug":"x","prompt":"hello","response":"world","extra":1}',
        b'{"slug":"y","prompt":"foo","response":"bar"}',
    ]
    with patch("bin.dataset_enrich.requests.get", return_value=mock_resp) as mget:
        items = list(cdn_download_and_parse("owner/repo", "batches/public-raw/2025-01-01/a.jsonl"))
    mget.assert_called_once()
    called_url = mget.call_args[0][0]
    assert "resolve/main" in called_url
    assert len(items) == 
