# axentx-dev-bot decision
- id: `20260503-034104-surrogate-1-discovery-afe42555`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T03:41:04.482670Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:41:04.482769Z

## Implementation Plan (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16` (matrix) and optional `DATE_FOLDER` (defaults to today `YYYY-MM-DD`)
- Uses **manifest-driven, CDN-bypass ingestion**: single API call to list one date folder → save `file-list.json`; workers stream files via raw CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) to avoid HF API rate limits during training
- Projects every file to `{prompt, response}` only at parse time (avoids pyarrow CastError on mixed schemas)
- Deduplicates via central `lib/dedup.py` md5 store
- Uploads shard output to `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`
- Adds shebang, `chmod +x`, and Bash-safe invocation for cron compatibility

---

## File: bin/dataset-enrich.py

```python
#!/usr/bin/env python3
"""
Manifest-driven, CDN-bypass ingestion worker for surrogate-1.

Usage (GitHub Actions matrix):
  SHARD_ID=0 SHARD_TOTAL=16 python bin/dataset-enrich.py

Env:
  SHARD_ID          - worker index (0..SHARD_TOTAL-1)
  SHARD_TOTAL       - total parallel workers (default 16)
  DATE_FOLDER       - dataset subfolder date (default today YYYY-MM-DD)
  HF_TOKEN          - write token for axentx/surrogate-1-training-pairs
  HF_REPO           - dataset repo (default axentx/surrogate-1-training-pairs)
  MANIFEST_PATH     - optional pre-saved file-list.json (if present, skips list_repo_tree)
"""

import os
import sys
import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

import requests
from huggingface_hub import HfApi, hf_hub_download, list_repo_tree

# ---- config ----
HF_REPO = os.getenv("HF_REPO", "axentx/surrogate-1-training-pairs")
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("ERROR: HF_TOKEN is required", file=sys.stderr)
    sys.exit(1)

SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
DATE_FOLDER = os.getenv("DATE_FOLDER", datetime.utcnow().strftime("%Y-%m-%d"))

API = HfApi(token=HF_TOKEN)

# paths
WORKDIR = Path(__file__).parent.parent
MANIFEST_PATH = Path(os.getenv("MANIFEST_PATH", WORKDIR / "file-list.json"))
DEDUP_PY = WORKDIR / "lib" / "dedup.py"
OUTPUT_DIR = WORKDIR / "batches" / "public-merged" / DATE_FOLDER
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---- helpers ----
def slug_hash(s: str) -> int:
    """Deterministic 0..2^32-1 hash for shard assignment."""
    return int(hashlib.md5(s.encode()).hexdigest(), 16) % (2**32)

def belongs_to_shard(slug: str) -> bool:
    return (slug_hash(slug) % SHARD_TOTAL) == SHARD_ID

def list_date_files() -> List[str]:
    """Single API call: list files in DATE_FOLDER (non-recursive)."""
    print(f"Listing repo tree: {HF_REPO} @ {DATE_FOLDER}")
    try:
        tree = list_repo_tree(
            repo_id=HF_REPO,
            path=DATE_FOLDER,
            repo_type="dataset",
            recursive=False,
        )
    except Exception as e:
        print(f"ERROR listing repo tree: {e}", file=sys.stderr)
        sys.exit(1)
    files = [item.rfilename for item in tree if item.type == "file"]
    print(f"Found {len(files)} files in {DATE_FOLDER}")
    return files

def save_manifest(files: List[str]) -> None:
    MANIFEST_PATH.write_text(json.dumps(files, indent=2))
    print(f"Saved manifest to {MANIFEST_PATH}")

def load_manifest() -> List[str]:
    if not MANIFEST_PATH.exists():
        return []
    return json.loads(MANIFEST_PATH.read_text())

def is_duplicate(md5_b64: str) -> bool:
    """Delegate to central dedup store (lib/dedup.py)."""
    # dedup.py exposes a small CLI: python lib/dedup.py check <md5>
    import subprocess
    try:
        out = subprocess.check_output(
            [sys.executable, str(DEDUP_PY), "check", md5_b64],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out == "1"
    except E

## review — reviewer @ 2026-05-03T03:41:09.304533Z

APPROVE: workable first-step implementation that establishes manifest-driven ingestion, shard partitioning, dedup integration, and CDN-bypass pattern; incremental progress with clear acceptance criteria a tester can validate.

Acceptance criteria:
- Script accepts SHARD_ID/SHARD_TOTAL and DATE_FOLDER env vars and exits non-zero when HF_TOKEN is missing.
- Single repo-tree API call produces file-list.json (or uses existing MANIFEST_PATH) and assigns files to shards deterministically via slug_hash.
- Worker streams files via raw CDN URLs and projects to {prompt, response} without requiring full schema uniformity (avoids pyarrow CastError on mixed schemas).
- Deduplication delegates to lib/dedup.py CLI (check/add) and tolerates dedup unavailability by safe fallback.
- Output shard written to batches/public-merged/{DATE_FOLDER}/shard{N}-{HHMMSS}.jsonl and script is executable (shebang + chmod +x) for cron/GA invocation.

## qa — qa @ 2026-05-03T03:41:24.343897Z

PASS: Implementation plan is workable and acceptance criteria are testable.

1. **Acceptance criteria**
- Script exits with non-zero code and prints ERROR when HF_TOKEN is missing or empty.
- With HF_TOKEN present, script accepts SHARD_ID (0..SHARD_TOTAL-1), SHARD_TOTAL (default 16), DATE_FOLDER (default today YYYY-MM-DD) and produces deterministic shard assignment via slug_hash modulo SHARD_TOTAL.
- Single repo-tree API call is made per run unless MANIFEST_PATH exists and is valid JSON; file-list.json is saved when listing succeeds.
- Each assigned file is streamed via raw CDN URL (https://huggingface.co/datasets/.../resolve/main/...) and parsed into {prompt, response} without requiring uniform schema (non-object/missing fields handled gracefully).
- Deduplication delegates to `python lib/dedup.py check/add <md5>` and, if dedup CLI fails or is unavailable, records are processed with a safe fallback (no crash, warning emitted).
- Output file is written to batches/public-merged/{DATE_FOLDER}/shard{N}-{HHMMSS}.jsonl with one JSON object per line; script has executable bit and valid shebang for cron/GA invocation.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_dataset_enrich_unit.py
import os
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
import dataset_enrich as mod

def test_slug_hash_deterministic():
    assert mod.slug_hash("abc") == mod.slug_hash("abc")
    assert 0 <= mod.slug_hash("x") < 2**32

def test_belongs_to_shard():
    with patch.dict(os.environ, {"SHARD_TOTAL": "16", "SHARD_ID": "3"}):
        mod.SHARD_TOTAL = 16
        mod.SHARD_ID = 3
        slug = "test-slug"
        expected = (mod.slug_hash(slug) % 16) == 3
        assert mod.belongs_to_shard(slug) == expected

def test_missing_hf_token_exits_nonzero(capsys):
    with patch.dict(os.environ, {}, clear=True):
        mod.HF_TOKEN = None
        try:
            mod.main()
        except SystemExit as e:
            assert e.code != 0
        captured = capsys.readouterr()
        assert "ERROR" in captured.err

def test_list_date_files_calls_list_repo_tree_once():
    with patch("dataset_enrich.list_repo_tree") as mock_list:
        mock_list.return_value = [MagicMock(path="2023-01-01/a.jsonl")]
        files = mod.list_date_files()
        assert mock_list.call_count == 1
        assert len(files) == 1

def test_save_manifest_writes_json(tmp_path):
    manifest = tmp_path / "file-list.json"
    items = ["a.jsonl", "b.jsonl"]
    mod._save_manifest(items, manifest)
    assert json.loads(manifest.read_text()) == items

def test_project_prompt_response_tolerates_mixed_schema():
    # raw record may be missing fields or have nested structures
    raw = {"prompt": "hi", "extra": {"x": 1}}
    out = mod._project_prompt_response(raw)
    assert out["prompt"] == "hi"
    assert out.get("response") is None or isinstance(out.get("response"), str)

    raw = {"messages": [{"role": "user", "content": "q"}, {"role": "assistant", "content": "a"}]}
    out = mod._project_prompt_response(raw)
    assert "prompt" in out and "response" in out

def test_dedup_cli_failure_safe_fallback(capsys):
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError("dedup missing")
        result = mod._dedup_check("abcd")
        assert result is False  # treat as not-seen when unavailable
        assert "WARNING" in capsys.readouterr().out
```

3. **Integration tests** (3 happy + 3 edge)
```text
Happy cases:
1) Full run with mocked HF API and CDN stream:
   - Pre-seed MANIFEST_PATH with 32 files across dates.
   - SHARD_TOTAL=4, SHARD_ID=1 -> worker processes only assigned files.
   - Mock list_repo_tree (once), mock raw CDN GET (200 + NDJSON lines).
   - Mock dedup CLI: first check miss -> add success.
   - Expect: output file exists under batches/public-merged/{today}/shard1-*.jsonl with deduplicated {prompt,response} lines.

2) Manifest reuse (skip list_repo_tree):
   - Provide valid MANIFEST_PATH fil
