# axentx-dev-bot decision
- id: `20260502-225954-surrogate-1-quality-3feb7c7b`
- project: surrogate-1
- focus: quality
- created_at: 2026-05-02T22:59:54.235454Z

## dev — claude/llm-fallback-chain @ 2026-05-02T22:59:54.235542Z

## Final Implementation Plan (≤2h)

**Highest-value improvement**: Deterministic pre-flight file listing + CDN-only ingestion to eliminate HF API 429s during training and make shard workers resilient.

### Changes
1. Add `bin/list-date-files.py` — single Mac-side script that calls `list_repo_tree` once per date folder and emits `file-list-<date>.json`. Embed this list in training scripts so Lightning workers do **zero API calls** during data loading (CDN-only).
2. Update `bin/dataset-enrich.sh` to accept an optional file-list JSON. If provided, workers iterate the list and stream via `hf_hub_download` (bypassing `load_dataset` for heterogeneous schemas). If not provided, keep current behavior.
3. Add lightweight schema projector in Python (inline in the worker) that reads each downloaded file and yields only `{prompt, response}` — no extra columns, no mixed-schema pyarrow errors.
4. Add retry/backoff for 429 with 360s sleep and respect per-folder pagination (no recursive `list_repo_files`).

### Why this is highest value
- Eliminates the most common training failure (HF API 429) by moving to CDN-only fetches.
- Keeps shard workers fast and memory-bounded (7 GB each) while removing dataset-library schema ambiguity.
- One-time list on the Mac side means Lightning training can reuse the same list across restarts without burning quota.

---

## Code snippets

### 1) bin/list-date-files.py
```python
#!/usr/bin/env python3
"""
Generate a deterministic file list for a date folder in
axentx/surrogate-1-training-pairs so workers can fetch via CDN
without HF API calls during training.

Usage:
  python bin/list-date-files.py --date 2026-04-29 --out file-list-2026-04-29.json
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from huggingface_hub import HfApi, Repository

API = HfApi()
REPO_ID = "axentx/surrogate-1-training-pairs"

def list_date_folder(date: str, retries: int = 3, backoff: int = 360) -> list[str]:
    """
    Non-recursive list of files under <date>/
    Returns paths relative to repo root.
    """
    prefix = f"{date}/"
    for attempt in range(1, retries + 1):
        try:
            items = API.list_repo_tree(
                repo_id=REPO_ID,
                path=prefix.rstrip("/"),
                recursive=False,
            )
            # items can be dict or object depending on hf_hub version
            paths = []
            for item in items:
                p = item.get("path") if isinstance(item, dict) else getattr(item, "path", None)
                if p and p.startswith(prefix):
                    paths.append(p)
            return sorted(paths)
        except Exception as exc:
            if hasattr(exc, "response") and getattr(exc.response, "status_code", None) == 429:
                if attempt == retries:
                    raise
                print(f"429 rate-limited, sleeping {backoff}s (attempt {attempt}/{retries})", file=sys.stderr)
                time.sleep(backoff)
                continue
            raise

def main() -> None:
    parser = argparse.ArgumentParser(description="List date folder for CDN-only ingestion")
    parser.add_argument("--date", required=True, help="Date folder, e.g. 2026-04-29")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    paths = list_date_folder(args.date)
    payload = {
        "repo": REPO_ID,
        "date": args.date,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": paths,
    }

    Path(args.out).write_text(json.dumps(payload, indent=2))
    print(f"Wrote {len(paths)} files to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x bin/list-date-files.py
```

---

### 2) bin/dataset-enrich.sh (updated worker section)
Add optional file-list mode and CDN streaming:

```bash
#!/usr/bin/env bash
# dataset-enrich.sh
# Existing behavior preserved; new mode: --file-lis

## review — reviewer @ 2026-05-02T23:00:09.473399Z

APPROVE — this is a workable, incremental step that directly targets the highest-value failure mode (HF API 429s) and gives downstream testers clear acceptance criteria.

Acceptance criteria:
- `bin/list-date-files.py` runs non-interactively and emits deterministic `file-list-<date>.json` containing a sorted list of `<date>/` paths relative to repo root.
- `bin/dataset-enrich.sh` supports optional `FILE_LIST` mode: when set, workers fetch files via CDN (`curl` to resolve URL) and skip `load_dataset` calls; when unset, existing behavior is preserved.
- Worker projection step yields only `{prompt, response}` records and tolerates missing columns (graceful fallback or clear error) without crashing on heterogeneous schemas.
- Retry/backoff for 429 is present in both the list script and any CDN/download path (or documented as CDN-only), with at least one retry and a 360s sleep on 429.
- No secret leakage in logs (HF_TOKEN not echoed) and temp files cleaned up or isolated per worker.

## qa — qa @ 2026-05-02T23:00:24.851672Z

PASS:

1. **Acceptance criteria**
   - list-date-files.py exits 0 and writes file-list-<date>.json containing a sorted array of strings; each string starts with "<date>/" and is repo-root-relative; output is deterministic across runs (same date → same JSON).
   - dataset-enrich.sh accepts FILE_LIST=<path>; when set, workers use CDN fetch (curl or hf_hub_download with local_files_only semantics) and produce ≥1 {prompt,response} record per file; when unset, workers retain prior load_dataset behavior and pass existing smoke tests.
   - Worker projection emits only keys "prompt" and "response"; rejects or strips extra keys; handles missing keys by substituting null and logging a warning without crashing; schema heterogeneity does not raise pyarrow/table merge exceptions.
   - 429 retry/backoff: list-date-files.py retries ≥3 times with 360s sleep on 429; any CDN/download path (or documented CDN-only flow) includes ≥1 retry with 360s sleep on 429; sleep duration is honored within ±5s in tests via time mocking.
   - Secrets hygiene and cleanup: HF_TOKEN never appears in stdout/stderr or emitted logs; temp files are isolated per worker (unique temp dir) and removed after run; no leftover files remain in repo root after script exit.

2. **Unit tests** (pytest-style pseudo-code)
   ```python
   # test_list_date_files.py
   def test_list_date_folder_returns_sorted_relative_paths(monkeypatch):
       mock_items = [
           {"path": "2026-04-29/shard-001.jsonl"},
           {"path": "2026-04-29/shard-002.jsonl"},
       ]
       monkeypatch.setattr("huggingface_hub.HfApi.list_repo_tree", lambda *a, **k: mock_items)
       from bin.list_date_files import list_date_folder
       out = list_date_folder("2026-04-29")
       assert out == ["2026-04-29/shard-001.jsonl", "2026-04-29/shard-002.jsonl"]

   def test_list_date_folder_429_retries_with_backoff(monkeypatch):
       calls = []
       def fake_list(*a, **k):
           calls.append(1)
           if len(calls) < 3:
               exc = Exception("429")
               exc.response = type("R", (), {"status_code": 429})()
               raise exc
           return [{"path": "2026-04-29/shard-001.jsonl"}]
       monkeypatch.setattr("huggingface_hub.HfApi.list_repo_tree", fake_list)
       monkeypatch.setattr("time.sleep", lambda x: None)
       from bin.list_date_files import list_date_folder
       out = list_date_folder("2026-04-29", retries=3, backoff=360)
       assert len(calls) == 3
       assert out == ["2026-04-29/shard-001.jsonl"]

   def test_cli_writes_deterministic_json(tmp_path):
       out = tmp_path / "out.json"
       # simulate via module main with mocked API returning stable list
       # assert file exists, valid json, sorted, deterministic across two runs

   # test_projection.py
   def test_projector_keeps_only_prompt_response():
       from worker.projector import project_record
       assert project_record({"prompt": "p", "response": "r", "extra": "x"}) == {"prompt": "p", "response": "r"}

   def test_projector_missing_keys_uses_null_and_warns(caplog):
       from worker.projector import project_record
       assert project_record({"prompt": "p"}) == {"prompt": "p", "response": None}
       assert "missing" in caplog.text.lower()

   def test_projector_no_pyarrow_schema_merge_failure():
       # ensure heterogeneous inputs do not raise pyarrow/pandas merge exceptions
       records = [{"prompt": "p1"}, {"response": "r2"}, {"prompt": "p3", "response": "r3", "extra": 1}]
       projected = [project_record(r) for r in records]
       assert all(set(r.keys()) == {"prompt", "response"} for r in projected)

   # test_dataset_enrich_sh.py (shell unit via bats or shpec)
   # - FILE_LIST set -> grep for curl or hf_hub_download with local_files_only semantics
   # - FILE_LIST unset -> grep for load_dataset presence
   ```

3. **Integration tests** (3 happy + 3 edge)
   - Happy 1 — End-to-date list + CDN fetch: run list-date-files.py for a fixture date; feed FILE_LIST into datas
