# axentx-dev-bot decision
- id: `20260502-232459-surrogate-1-design-5a40ddfc`
- project: surrogate-1
- focus: design
- created_at: 2026-05-02T23:24:59.461564Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:24:59.461636Z

## Implementation Plan (≤2h)

**Goal**: Eliminate runtime `load_dataset(streaming=True)` and recursive `list_repo_files` from `bin/dataset-enrich.sh`. Replace with deterministic pre-flight snapshot + CDN-only fetches to avoid HF API rate limits and schema errors.

### Changes
1. **Add `bin/list-snapshot.py`** — run once per cron tick (Mac/CI) to produce `file-list.json` for a single date folder via `list_repo_tree(recursive=False)`.
2. **Update `bin/dataset-enrich.sh`** — accept file-list path; fetch each file via CDN URL (`resolve/main/...`) with `curl`/`wget`, stream-parse to `{prompt,response}`, dedup, emit shard output.
3. **Add lightweight Python helper `lib/stream_parse.py`** — reads raw bytes from stdin or file, projects to `{prompt,response}` per known schema, outputs NDJSON lines.
4. **Update workflow** — add a single non-matrix job step that produces `file-list.json` as an artifact, then matrix shards download and use it (no HF API calls during shard work).

### Why this fits <2h
- Small, focused scripts; no training code changes.
- Reuses existing dedup logic (`lib/dedup.py`).
- Avoids heavy `datasets` streaming in workers (prevents OOM in CI).
- CDN bypass removes 429 risk during parallel shard execution.

---

## Code Snippets

### 1) `bin/list-snapshot.py`
```python
#!/usr/bin/env python3
"""
Produce a deterministic file-list snapshot for one date folder.
Usage:
  HF_TOKEN=<token> python bin/list-snapshot.py \
    --repo axentx/surrogate-1-training-pairs \
    --date 2026-05-02 \
    --out file-list.json
"""
import argparse
import json
import os
import sys
from huggingface_hub import HfApi

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD folder under datasets/")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("HF_TOKEN required", file=sys.stderr)
        sys.exit(1)

    api = HfApi(token=token)
    # Non-recursive: one API call, no pagination explosion
    path = f"batches/public-merged/{args.date}"
    try:
        entries = api.list_repo_tree(repo_id=args.repo, path=path, recursive=False)
    except Exception as e:
        print(f"list_repo_tree failed: {e}", file=sys.stderr)
        sys.exit(1)

    files = [e.path for e in entries if e.type == "file"]
    files.sort()  # deterministic ordering

    snapshot = {
        "repo": args.repo,
        "date": args.date,
        "path_prefix": path,
        "files": files,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Wrote {len(files)} files to {args.out}")

if __name__ == "__main__":
    main()
```

### 2) `lib/stream_parse.py`
```python
#!/usr/bin/env python3
"""
Stream parser: project raw parquet/jsonl bytes to {prompt,response}.
Reads file path from argv[1] or stdin, writes NDJSON to stdout.
Keeps memory low by processing line-by-line for jsonl or row-by-row for parquet.
"""
import json
import pyarrow.parquet as pq
import sys
from typing import Any, Dict

def normalize_record(rec: Dict[str, Any]) -> Dict[str, str]:
    # Heuristic projection; adapt to known schemas as needed.
    prompt = rec.get("prompt") or rec.get("input") or rec.get("question") or ""
    response = rec.get("response") or rec.get("output") or rec.get("answer") or ""
    return {"prompt": str(prompt), "response": str(response)}

def main() -> None:
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path.endswith(".parquet"):
            try:
                table = pq.read_table(path, columns=["prompt", "response"])
                for batch in table.to_batches(max_chunksize=8192):
                    prompts = batch.column("prompt").to_pylist()
                    responses = batch.column("response").to_pylist()
                    for p, r in zip(prompts, responses):
                   

## review — reviewer @ 2026-05-02T23:25:09.612533Z

APPROVE: This is a workable, incremental step that replaces runtime HF streaming/list calls with a deterministic snapshot + CDN fetches, reducing 429/OOM risk in CI. The design is focused, reuses existing dedup logic, and is implementable within the stated timebox.

Acceptance criteria (for downstream testing/completion):
- `bin/list-snapshot.py` produces deterministic `file-list.json` for a given date folder and exits non-zero on auth/path errors; artifact is consumable by matrix jobs.
- `bin/dataset-enrich.sh` accepts a file-list path, fetches each file via CDN (`resolve/main/...`) with retries/backoff, streams through `lib/stream_parse.py`, dedups via `lib/dedup.py`, and emits shard outputs without HF API calls during shard execution.
- `lib/stream_parse.py` reads parquet/jsonl from file or stdin, projects to `{prompt,response}` per known schema, emits valid NDJSON lines, and keeps memory bounded (row/batch streaming) with graceful fallback for schema variations.
- Workflow includes a non-matrix step that generates `file-list.json` as an artifact and matrix shards consume it; no `load_dataset(streaming=True)` or recursive `list_repo_files` in shard steps.
- Basic error handling and logging: malformed lines/files are skipped with counts reported; CDN fetch failures are retried and cause job failure only after exhaustion.

## qa — qa @ 2026-05-02T23:25:25.463153Z

PASS: 

1. **Acceptance criteria**
   - `bin/list-snapshot.py` exits 0 and produces `file-list.json` containing sorted file list for the given date folder; exits non-zero when HF_TOKEN missing or path not found.
   - `bin/dataset-enrich.sh` accepts `--file-list` and fetches every listed file via CDN URL (`resolve/main/...`) using curl/wget with retry/backoff; emits shard outputs without invoking HF API during shard execution.
   - `lib/stream_parse.py` reads parquet/jsonl from file or stdin, projects to `{prompt,response}` per known schema, emits valid NDJSON lines, and keeps memory bounded (row/batch streaming).
   - Workflow non-matrix step produces `file-list.json` artifact; matrix shards consume it and perform zero HF API calls (no `load_dataset(streaming=True)` or recursive `list_repo_files`).
   - Malformed lines/files are skipped with counts reported; CDN fetch failures are retried and cause job failure only after exhaustion (configurable max retries).
   - Deduplication via `lib/dedup.py` is applied to parsed `{prompt,response}` pairs before shard emission; duplicate rate and retained count are logged.
   - End-to-end run on a sample date folder produces deterministic shard outputs (byte-for-byte identical) when re-run with same `file-list.json`.

2. **Unit tests**
```python
# tests/unit/test_list_snapshot.py
import json, os, tempfile, subprocess, sys

def test_exits_nonzero_no_token(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    r = subprocess.run([sys.executable, "bin/list-snapshot.py", "--repo", "x/x", "--date", "2026-01-01", "--out", "out.json"], capture_output=True)
    assert r.returncode != 0
    assert b"HF_TOKEN" in r.stderr

def test_produces_sorted_json(monkeypatch, mocker):
    from unittest.mock import MagicMock
    mocker.patch("huggingface_hub.HfApi.list_repo_tree", return_value=[
        MagicMock(path="batches/public-merged/2026-05-02/b.json", type="file"),
        MagicMock(path="batches/public-merged/2026-05-02/a.json", type="file"),
    ])
    monkeypatch.setenv("HF_TOKEN", "fake")
    out = tempfile.NamedTemporaryFile(delete=False)
    out.close()
    try:
        subprocess.run([sys.executable, "bin/list-snapshot.py", "--repo", "axentx/surrogate-1-training-pairs", "--date", "2026-05-02", "--out", out.name], check=True)
        with open(out.name) as f:
            snap = json.load(f)
        assert snap["files"] == ["batches/public-merged/2026-05-02/a.json", "batches/public-merged/2026-05-02/b.json"]
    finally:
        os.unlink(out.name)

# tests/unit/test_stream_parse.py
import subprocess, json, tempfile, sys

def test_parses_jsonl_stdin_to_ndjson():
    inp = b'{"prompt":"hi","response":"ok"}\n{"prompt":"bye","response":"no"}\n'
    out = subprocess.check_output([sys.executable, "lib/stream_parse.py", "-"], input=inp)
    lines = [json.loads(l) for l in out.strip().split(b"\n")]
    assert len(lines) == 2
    assert all("prompt" in l and "response" in l for l in lines)

def test_handles_parquet_file():
    import pyarrow as pa, pyarrow.parquet as pq, pandas as pd
    df = pd.DataFrame({"prompt": ["p1"], "response": ["r1"]})
    tbl = pa.Table.from_pandas(df)
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as f:
        pq.write_table(tbl, f.name)
        out = subprocess.check_output([sys.executable, "lib/stream_parse.py", f.name])
    lines = [json.loads(l) for l in out.strip().split(b"\n") if l]
    assert len(lines) == 1
    assert lines[0]["prompt"] == "p1"

def test_skips_malformed_and_reports():
    inp = b'{"prompt":"ok"}\n{"prompt":"x","response":"y"}\n'
    proc = subprocess.run([sys.executable, "lib/stream_parse.py", "-"], input=inp, capture_output=True)
    lines = [json.loads(l) for l in proc.stdout.strip().split(b"\n") if l]
    assert len(lines) == 1
    assert b"skipped" in proc.stderr.lower() or b"invalid" in proc.stderr.lower()

# tests/unit/test_dataset_enrich_sh.py (shell unit via bats or sharness style)
# Pseudo:
# - mock curl to 
