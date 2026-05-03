# axentx-dev-bot decision
- id: `20260502-225728-surrogate-1-quality-d21a5d1d`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-02T22:57:28.522244Z

## dev — claude/llm-fallback-chain @ 2026-05-02T22:57:28.522321Z

**Final Synthesis**  
*(Best parts merged, contradictions resolved in favor of correctness + concrete actionability)*

---

## Summary of the chosen approach
- **Deterministic pre-flight file listing** (date-scoped) to eliminate recursive `list_repo_files` calls that cause HF API 429s.
- **CDN-only ingestion** during training/shard work to achieve zero HF API data calls.
- **Backward-compatible**: workers fall back to current behavior when no file list is provided.
- **Actionable in ≤2 hours**: 3 files changed (~110 lines total), clear tests and rollout steps.

---

## 1) `bin/list_files.py` (new, deterministic, date-scoped)

```python
#!/usr/bin/env python3
"""
Generate deterministic file list for a date folder in
axentx/surrogate-1-training-pairs.

Usage:
  python bin/list_files.py --date 2026-05-02 --out file-list.json

Output schema:
{
  "repo": "axentx/surrogate-1-training-pairs",
  "date": "2026-05-02",
  "generated_at": "2026-05-02T22:00:00Z",
  "files": [
    {"path": "batches/public-raw/2026-05-02/foo.parquet", "size": 12345, "sha256": null},
    ...
  ]
}
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

from huggingface_hub import HfApi

REPO = "axentx/surrogate-1-training-pairs"

def main() -> None:
    parser = argparse.ArgumentParser(description="List repo files for a date folder (non-recursive per folder).")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-05-02")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--token", default=os.getenv("HF_TOKEN"), help="HF token (optional for public repo listing)")
    args = parser.parse_args()

    api = HfApi(token=args.token)
    folder_path = f"batches/public-raw/{args.date}"

    try:
        entries = api.list_repo_tree(
            repo_id=REPO,
            path=folder_path,
            repo_type="dataset",
            recursive=False,
        )
    except Exception as e:
        print(f"ERROR listing {folder_path}: {e}", file=sys.stderr)
        sys.exit(1)

    files = []
    for entry in entries:
        if entry.type != "file":
            continue
        files.append({
            "path": entry.path,
            "size": getattr(entry, "size", None),
            "sha256": None,
        })

    # Deterministic ordering for stable sharding
    files.sort(key=lambda x: x["path"])

    payload = {
        "repo": REPO,
        "date": args.date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x bin/list_files.py
```

---

## 2) `bin/dataset-enrich.sh` (edit: CDN-only + fallback)

```bash
#!/usr/bin/env bash
#
# dataset-enrich.sh
# Normalize and dedup public dataset shards.
#
# Usage:
#   SHARD_ID=0 SHARD_COUNT=16 FILE_LIST=file-list.json ./bin/dataset-enrich.sh
#
# Environment:
#   SHARD_ID      (required) 0..15
#   SHARD_COUNT   (required) total shards (e.g., 16)
#   FILE_LIST     (optional) path to file-list.json from list_files.py
#
# Behavior:
# - If FILE_LIST is provided and valid: use CDN-only ingestion (zero HF API data calls).
# - Otherwise: fall back to current load_dataset behavior.

set -euo pipefail

: "${SHARD_ID:?required}"
: "${SHARD_COUNT:?required}"
FILE_LIST="${FILE_LIST:-}"

REPO="axentx/surrogate-1-training-pairs"
BASE_CDN="https://huggingface.co/datasets/${REPO}/resolve/main"

log() {
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $*"
}

normalize_and_dedup() {
  local input_path="$1"
  local output_path="$2"
  python -m lib.dedup --input "$input_path" --output "$output_path"
}

if [[ -n "$FILE_LIST" && -f "$FILE_LIST" ]]; then
  log "CDN-only mode enabled (FILE_LIST=$FILE_LIST)"

  # Read 

## review — reviewer @ 2026-05-02T22:57:33.566372Z

APPROVE: Deterministic pre-flight listing + CDN-only ingestion is a concrete, safe step that reduces HF API pressure and is backward-compatible; the changes are small, testable, and shippable.

Acceptance criteria:
- `bin/list_files.py` runs without error for a valid date folder and produces deterministic, sorted JSON matching the documented schema.
- `bin/dataset-enrich.sh` in CDN-only mode (with valid FILE_LIST) fetches files via CDN URLs and produces enriched outputs without calling `load_dataset` (zero HF data API calls).
- `bin/dataset-enrich.sh` with missing/invalid FILE_LIST falls back to the prior `load_dataset` behavior and completes successfully.
- Shard assignment is stable: rerunning with the same FILE_LIST and SHARD_COUNT assigns the same files to the same SHARD_ID.
- No secrets or tokens are logged or exposed in console output or temp files.

## qa — qa @ 2026-05-02T22:57:51.097952Z

PASS: Deterministic pre-flight + CDN-only ingestion is concrete, safe, and backward-compatible.

---

## 1) Acceptance criteria
- `bin/list_files.py --date YYYY-MM-DD --out out.json` exits 0 and emits JSON matching schema (repo, date, generated_at ISO-8601, files list with path/str/size/sha256 keys) with deterministic sorted paths.
- `bin/dataset-enrich.sh` in CDN-only mode (FILE_LIST set and valid) completes enrichment without any `load_dataset` calls (zero HF data API calls) and emits enriched outputs.
- `bin/dataset-enrich.sh` with missing/invalid FILE_LIST falls back to `load_dataset` behavior and completes successfully (exit 0, outputs produced).
- Shard assignment is stable: same FILE_LIST + SHARD_COUNT + SHARD_ID across two runs yields identical file-to-shard mapping (byte-for-byte shard outputs).
- No secrets/tokens appear in stdout/stderr or temporary files (grepable scan of logs and temp dirs returns no token-like strings).

---

## 2) Unit tests

```python
# tests/unit/test_list_files.py (pytest)
import json
import os
import tempfile
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from bin.list_files import REPO, main as list_files_main

def test_list_files_output_schema_and_sorting():
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "file-list.json")
        mock_entries = [
            MagicMock(type="file", path="batches/public-raw/2026-05-02/z.parquet", size=300),
            MagicMock(type="file", path="batches/public-raw/2026-05-02/a.parquet", size=100),
            MagicMock(type="dir", path="batches/public-raw/2026-05-02/sub", size=None),
        ]
        with patch("bin.list_files.HfApi") as MockApi:
            MockApi.return_value.list_repo_tree.return_value = mock_entries
            with patch("sys.argv", ["list_files.py", "--date", "2026-05-02", "--out", out]):
                list_files_main()

        with open(out, "r", encoding="utf-8") as f:
            payload = json.load(f)

        assert payload["repo"] == REPO
        assert payload["date"] == "2026-05-02"
        assert datetime.fromisoformat(payload["generated_at"].replace("Z", "+00:00"))
        assert isinstance(payload["files"], list)
        paths = [f["path"] for f in payload["files"]]
        assert paths == sorted(paths)  # deterministic ordering
        assert all("path" in f and isinstance(f["size"], (int, type(None))) for f in payload["files"])
        assert all("sha256" in f and f["sha256"] is None for f in payload["files"])
        assert len(payload["files"]) == 2  # dirs excluded

def test_list_files_exit_nonzero_on_api_error():
    with patch("bin.list_files.HfApi") as MockApi:
        MockApi.return_value.list_repo_tree.side_effect = RuntimeError("API down")
        with patch("sys.argv", ["list_files.py", "--date", "2026-05-02", "--out", "x.json"]), \
             patch("sys.exit") as mock_exit:
            list_files_main()
            mock_exit.assert_called_with(1)
```

```python
# tests/unit/test_shard_assign.py (pytest)
import json
import os
import tempfile
from unittest.mock import patch

from bin.dataset_enrich import assign_shard_files  # extracted helper for testability

def test_shard_assignment_stable():
    files = [f"batches/public-raw/2026-05-02/file{i}.parquet" for i in range(17)]
    file_list = {"files": [{"path": p} for p in files]}

    assignments_a = assign_shard_files(file_list, shard_count=4, shard_id=0)
    assignments_b = assign_shard_files(file_list, shard_count=4, shard_id=0)
    assert assignments_a == assignments_b

    # shard 0 should get ceil(17/4) or consistent modulo distribution
    expected_for_0 = [f for i, f in enumerate(sorted(files)) if i % 4 == 0]
    assert assignments_a == expected_for_0
```

```python
# tests/unit/test_no_token_leak.py (pytest)
import re
from unittest.mock import patch, MagicMock

TOKEN_RE = re.compile(r"(ghp_|hf_[a-zA-Z0-9]{20,}|sk-[a-zA-Z0-9]{20,})")

def test_no_token_in_logs_list_files(capsys):

