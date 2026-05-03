# axentx-dev-bot decision
- id: `20260502-232354-surrogate-1-discovery-6b9cff68`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T23:23:54.815519Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:23:54.815594Z

## Final Implementation Plan (≤2h)

**Goal**: Eliminate runtime `load_dataset(streaming=True)` and recursive `list_repo_files` from `bin/dataset-enrich.sh`. Replace with deterministic pre-flight snapshot + CDN-only fetches to avoid HF API rate limits and schema heterogeneity issues.

### Steps (est. 90 min)

1. **Add snapshot utility** (`bin/make-snapshot.py`)  
   - Run once on Mac (or cron before the 16-shard matrix)  
   - Calls `list_repo_tree(path, recursive=False)` per date folder (non-recursive)  
   - Emits `snapshot-{date}.json` with `{file_path, size, sha, url}` for every parquet/jsonl  
   - Stores in repo under `snapshots/` (committed or artifact) so shards consume zero API calls during ingest

2. **Update `bin/dataset-enrich.sh`**  
   - Accept snapshot path as arg: `dataset-enrich.sh <snapshot.json> <shard_id> <nshards>`  
   - Remove `load_dataset` and `list_repo_files` calls  
   - Filter files by `shard_id = hash(slug) % nshards` using deterministic hash  
   - Download via CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) with `curl --retry 3 --retry-delay 5 -L -o`  
   - Stream-parse each file and project to `{prompt, response}` only; drop other columns  
   - Keep existing dedup via `lib/dedup.py` and output `batches/public-merged/<date>/shard<N>-<HHMMSS>.jsonl`

3. **Add lightweight Python fetcher** (`bin/fetch_cdn.py`)  
   - Reads snapshot, filters by shard, yields local temp paths  
   - Uses `requests` with streaming to avoid large memory peaks  
   - Emits line-delimited JSON records for shell pipeline

4. **Update GitHub Actions matrix**  
   - Add step before matrix to generate/restore snapshot artifact (or commit snapshots)  
   - Pass snapshot path to each shard via `with:` env  
   - Keep 16-shard parallelism unchanged

5. **Validation & rollback**  
   - Dry-run snapshot against a single shard locally  
   - Verify output row counts and schema match previous run  
   - Keep old codepath behind flag for one release (e.g., `USE_LEGACY_LOAD=0`)

---

## Code Snippets

### bin/make-snapshot.py
```python
#!/usr/bin/env python3
"""
Generate deterministic snapshot for a date folder.
Usage:
  python make-snapshot.py axentx/surrogate-1-training-pairs 2026-05-01 > snapshots/2026-05-01.json
"""
import json, hashlib, sys, os
from huggingface_hub import HfApi

API = HfApi()

def snapshot(repo_id: str, date_folder: str):
    # non-recursive per folder to avoid 100x pagination and 429
    tree = API.list_repo_tree(repo_id=repo_id, path=date_folder, recursive=False)
    files = []
    for f in tree:
        if f.path.endswith((".parquet", ".jsonl")):
            files.append({
                "path": f.path,
                "size": f.size,
                "sha": f.lfs.get("sha256", None) if f.lfs else None,
                # CDN URL — no Authorization header required
                "cdn": f"https://huggingface.co/datasets/{repo_id}/resolve/main/{f.path}"
            })
    # deterministic ordering
    files.sort(key=lambda x: x["path"])
    out = {
        "repo_id": repo_id,
        "date": date_folder,
        "generated_by": "make-snapshot.py",
        "files": files
    }
    return out

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: make-snapshot.py <repo_id> <date_folder>", file=sys.stderr)
        sys.exit(1)
    repo_id, date_folder = sys.argv[1], sys.argv[2]
    print(json.dumps(snapshot(repo_id, date_folder), indent=2))
```

### bin/fetch_cdn.py
```python
#!/usr/bin/env python3
"""
Yield records from snapshot for a single shard.
Usage:
  python fetch_cdn.py snapshot.json <shard_id> <nshards>
"""
import json, sys, hashlib, requests, tempfile, os

def shard_key(path: str, n: int) -> int:
    # deterministic across runs and platforms
    return int(hashlib.md5(path.encode()).hexdigest(), 16) % n

def stream_cdn(url: str):
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        # yield raw bytes; caller decodes per extens

## review — reviewer @ 2026-05-02T23:24:09.703805Z

APPROVE: Proposes a clear, incremental path to eliminate runtime HF API calls and recursive listing; snapshot + CDN-only fetches are a workable fix for rate limits and schema heterogeneity. Acceptance criteria below.

- Snapshot utility (`make-snapshot.py`) produces deterministic `snapshot-{date}.json` with `file_path`, `size`, `sha`, `cdn` for every parquet/jsonl in the date folder and sorts outputs for reproducibility.  
- `dataset-enrich.sh` accepts `<snapshot.json> <shard_id> <nshards>`, removes `load_dataset`/`list_repo_files`, filters files by `hash(path) % nshards == shard_id`, downloads via CDN URLs with retries, and streams parses to `{prompt,response}` only; dedup and output path conventions remain unchanged.  
- Lightweight fetcher (`fetch_cdn.py`) streams CDN content to temp files and yields local paths or line-delimited records without materializing entire files in memory; errors raise/exit non-zero for pipeline detection.  
- GitHub Actions matrix includes a pre-step to generate or restore the snapshot artifact (or uses committed snapshots) and passes the snapshot path to each shard; 16-shard parallelism is preserved.  
- Validation and rollback: dry-run one shard locally and verify row counts and schema match prior run; optional `USE_LEGACY_LOAD` flag (or similar) can restore old codepath for one release.

## qa — qa @ 2026-05-02T23:24:24.441799Z

PASS: 

1. **Acceptance criteria**
   - Snapshot utility emits valid JSON array sorted by `path`; every parquet/jsonl entry contains `path`, `size` (int ≥ 0), `sha` (string or null), `cdn` (valid HTTPS URL).
   - `dataset-enrich.sh` with `<snapshot.json> <shard_id> <nshards>` produces identical `{prompt,response}` schema and row count (±0) vs legacy run for the same deterministic shard assignment.
   - File-to-shard assignment is deterministic: `hash(path) % nshards == shard_id` yields same shard across runs; union of all shards covers all snapshot files with zero overlap.
   - CDN downloads use `curl --retry 3 --retry-delay 5 -L`; any single download failure after retries exits non-zero and logs the failing URL.
   - `fetch_cdn.py` streams to temp files without loading entire file into memory (peak RSS ≤ 2× largest file) and emits line-delimited JSON records or local paths; failure raises/exit non-zero.
   - GitHub Actions matrix pre-step provides snapshot artifact or committed snapshot; each shard receives snapshot path via env and completes without HF API calls (zero `list_repo_tree`/`load_dataset` invocations).
   - Optional `USE_LEGACY_LOAD=1` restores previous codepath and produces identical output to prior run for same inputs.

2. **Unit tests**
```python
# tests/unit/test_make_snapshot.py
def test_snapshot_sorted_and_valid():
    out = run_make_snapshot("axentx/surrogate-1-training-pairs", "2026-05-01")
    data = json.loads(out)
    assert isinstance(data, list)
    paths = [f["path"] for f in data]
    assert paths == sorted(paths)
    for f in data:
        assert "path" in f and f["path"].endswith((".parquet", ".jsonl"))
        assert isinstance(f["size"], int) and f["size"] >= 0
        assert f.get("sha") is None or isinstance(f["sha"], str)
        assert f["cdn"].startswith("https://huggingface.co/datasets/")

def test_snapshot_filters_non_parquet_jsonl():
    out = run_make_snapshot("axentx/surrogate-1-training-pairs", "2026-05-01")
    data = json.loads(out)
    for f in data:
        assert f["path"].endswith((".parquet", ".jsonl"))

# tests/unit/test_fetch_cdn.py
def test_fetch_cdn_streams_to_temp_and_yields_records(tmp_path):
    snapshot = [{"path": "2026-05-01/test.jsonl", "cdn": mock_cdn_url(tmp_path / "test.jsonl")}]
    records = list(fetch_cdn(snapshot, shard_id=0, nshards=1, tmp_dir=tmp_path))
    assert len(records) > 0
    for r in records:
        assert "prompt" in r and "response" in r

def test_fetch_cdn_failure_exits_nonzero(monkeypatch):
    monkeypatch.setattr("requests.get", lambda *a, **kw: exec('raise ConnectionError'))
    with pytest.raises(SystemExit, match="non-zero"):
        list(fetch_cdn([{"path": "x", "cdn": "https://fail"}], 0, 1))

# tests/unit/test_shard_assignment.py
def test_shard_assignment_deterministic():
    paths = ["a/1.parquet", "a/2.parquet", "b/1.jsonl"]
    assignments = [shard_for(p, nshards=4) for p in paths]
    for p, s in zip(paths, assignments):
        assert s == shard_for(p, nshards=4)

def test_shard_union_and_no_overlap():
    files = [{"path": f"2026-05-01/{i}.parquet"} for i in range(100)]
    by_shard = group_by_shard(files, nshards=16)
    union = []
    for s in range(16):
        union.extend(by_shard[s])
    assert sorted(union, key=lambda f: f["path"]) == sorted(files, key=lambda f: f["path"])
    # no overlap
    for i in range(16):
        for j in range(i + 1, 16):
            assert set(by_shard[i]) & set(by_shard[j]) == set()
```

3. **Integration tests**
```python
# Happy paths
def test_integration_single_shard_dry_run(tmp_path, snapshot_file):
    out_dir = tmp_path / "out"
    run_dataset_enrich(snapshot_file, shard_id=0, nshards=1, out_dir=out_dir)
    out_files = list(out_dir.glob("*.jsonl"))
    assert len(out_files) == 1
    records = [json.loads(l) for l in out_files[0].read_text().strip().splitlines()]
    for r in records:
        assert {"prompt", "response"} <= r.keys()
    # schema matches legacy
    legacy = run_legacy_shard
