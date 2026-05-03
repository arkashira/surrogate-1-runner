# axentx-dev-bot decision
- id: `20260503-011324-surrogate-1-discovery-7fbb4d72`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T01:13:24.266568Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:13:24.266731Z

## Final Synthesis (Best Parts + Correctness + Actionability)

Below is the single, production-ready plan that merges the strongest elements of both proposals, resolves contradictions, and prioritizes correctness and concrete actionability.

---

## Goal (unchanged)
Eliminate HF API rate-limit failures and HF Space OOM by replacing recursive `list_repo_files` and per-file API calls with **one per-folder `list_repo_tree` + CDN-only fetches**, and project to `{prompt,response}` at parse time—while preserving 16-shard parallelism.

---

## Core Decisions (Resolved Contradictions)
1. **Manifest strategy**: generate once per date folder and **commit to repo** (not ephemeral CI artifact).  
   - Why: both proposals agree this removes auth-bound API calls during shard runs; committing ensures reproducibility and fallback safety.

2. **Download method**: prefer **CDN direct fetch** (`resolve/main/...`) for files; keep `hf_hub_download` only as fallback for private repos.  
   - Why: CDN bypasses `/api/` rate limits and is faster; both proposals prefer this.

3. **Projection**: strict `{prompt,response}` only; drop all other fields at parse time to bound memory.  
   - Why: prevents OOM and schema drift; both proposals require this.

4. **No `load_dataset(streaming=True)` on full repo**: use per-file streaming decode instead.  
   - Why: avoids pyarrow CastError on heterogeneous repos; both proposals reject full-repo streaming.

5. **Shard assignment**: deterministic slice of manifest file list (not by file size or content hash) to keep logic simple and reproducible.  
   - Why: Candidate 1’s per-shard slicing is simpler and sufficient; Candidate 2’s size-based weighting adds complexity with little gain for this workload.

---

## Implementation Plan (≤2h)

### 1) Manifest generator (run once per date folder)
- Run on dev machine or in a short pre-job.
- Use `list_repo_tree(..., recursive=False)` for `public-merged/YYYY-MM-DD`.
- Save `manifests/YYYY-MM-DD.json` and **commit to repo**.
- Schema:
  ```json
  {
    "repo_id": "axentx/surrogate-1-training-pairs",
    "date": "YYYY-MM-DD",
    "root": "public-merged/YYYY-MM-DD",
    "files": ["rel/path1.parquet", "rel/path2.jsonl", ...]
  }
  ```

### 2) GitHub Actions (`ingest.yml`) changes
- Add a step before the matrix to compute `MANIFEST_URL` (CDN raw URL) and `MANIFEST_PATH` (repo-relative).
- Pass `MANIFEST_URL` and `TODAY` to each shard job.
- Keep the 16-shard matrix unchanged.
- Optional: add a pre-flight check that the manifest exists; fail fast if not.

### 3) Update `bin/dataset-enrich.sh`
- Accept `MANIFEST_URL` (preferred) or fall back to repo tree with warning.
- Download manifest via CDN (`curl`).
- Deterministically assign shard slice:
  - `TOTAL=${#FILES[@]}`
  - `PER_SHARD=$(( (TOTAL + TOTAL_SHARDS - 1) / TOTAL_SHARDS ))`
  - `START=$(( SHARD_ID * PER_SHARD ))`
  - `END=$(( START + PER_SHARD ))` (clamp to `TOTAL`)
- For each assigned file:
  - Fetch via CDN (`curl`) to temp file.
  - Stream-parse with projection helper.
  - Append `{prompt,response}` to shard output.
  - Clean up temp file immediately.
- Stream output to `batches/public-merged/YYYY-MM-DD/shard-<ID>-<TS>.jsonl`.

### 4) Python projection helper (`tools/parse_and_project.py`)
- Support `.parquet` and `.jsonl`.
- For `.parquet`: use `pyarrow.parquet.ParquetFile` with `iter_batches` to bound memory.
- For `.jsonl`: line-by-line streaming.
- Projection:
  - `prompt` = first non-empty of `prompt`, `input`, `text`.
  - `response` = first non-empty of `response`, `output`, `completion`.
  - Drop rows where either is empty.
  - Emit one JSON object per line (no extra fields).
- Robustness:
  - Skip malformed lines/batches with warnings to stderr.
  - Do not crash on single bad file.

### 5) Validation checklist (run locally before merge)
- Generate manifest for one date folder.
- Run one shard locally with `MANIFEST_URL` pointing to local file or CDN.
- Verify:
  - No 429s during listing or downloads.
  - Peak m

## review — reviewer @ 2026-05-03T01:13:29.979883Z

APPROVE: This is a clear, actionable “good first step” that directly targets HF API rate limits and OOM by replacing recursive per-file API calls with a single folder-level tree listing + CDN fetches, commits manifests for reproducibility, and keeps 16-shard parallelism with deterministic slicing. It proposes concrete, parsable artifacts and validation steps a downstream tester can check.

Acceptance criteria (for this discovery-stage change):
- Manifest generator produces `manifests/YYYY-MM-DD.json` containing `repo_id`, `date`, `root`, and sorted `files` array for one date folder.
- GitHub Actions workflow exposes `MANIFEST_URL` (CDN raw) and `TODAY` to each shard job and fails fast if the manifest is missing.
- Shard assignment uses deterministic slice (`TOTAL`, `PER_SHARD`, `START`, `END`) so every file in the manifest is assigned to exactly one shard and processed once.
- Per-file download prefers CDN (`curl resolve/main/...`) with `hf_hub_download` fallback for private repos; temp files are cleaned up immediately after parsing.
- Projection helper streams `.parquet` (pyarrow `iter_batches`) and `.jsonl` line-by-line, emits only `{prompt, response}` rows, skips malformed entries with warnings, and never loads the full repo into memory.

## qa — qa @ 2026-05-03T01:13:41.471365Z

PASS

1. **Acceptance criteria**
- Manifest generator produces `manifests/YYYY-MM-DD.json` with required keys (`repo_id`, `date`, `root`, `files`) and `files` is a non-empty, sorted array of strings for the target date folder.
- GitHub Actions exposes `MANIFEST_URL` (CDN raw) and `TODAY` to each shard job; workflow fails fast (non-zero exit) if the manifest file is missing or unreachable.
- Deterministic shard assignment assigns every manifest file to exactly one shard and no file is assigned to more than one shard (coverage = 100%, no duplicates).
- Per-file download prefers CDN (`curl resolve/main/...`) and falls back to `hf_hub_download` for private repos; temp files are removed immediately after parse (no residual temp files remain).
- Projection streams `.parquet` via pyarrow `iter_batches` and `.jsonl` line-by-line, emits only `{prompt, response}` rows, skips malformed entries with warnings, and peak memory stays bounded (no full-repo load).
- End-to-end shard run processes assigned files and emits a non-empty output dataset with schema `{prompt: str, response: str}`.
- Reproducibility: given the same manifest and shard count, shard assignment produces identical slices across runs.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_manifest_generator.py
def test_manifest_has_required_keys(tmp_path):
    out = generate_manifest(repo_id="axentx/surrogate-1-training-pairs", date="2024-06-01", root="public-merged/2024-06-01", files=["a.parquet"])
    assert out["repo_id"] == "axentx/surrogate-1-training-pairs"
    assert out["date"] == "2024-06-01"
    assert out["root"] == "public-merged/2024-06-01"
    assert out["files"] == ["a.parquet"]

def test_files_sorted_and_non_empty():
    out = generate_manifest(..., files=["b.parquet", "a.parquet"])
    assert out["files"] == ["a.parquet", "b.parquet"]

# test_shard_assignment.py
def test_deterministic_coverage_no_duplicates():
    files = [f"f{i}.parquet" for i in range(100)]
    shards = assign_shards(files, total_shards=16)
    assigned = [f for shard in shards.values() for f in shard]
    assert sorted(assigned) == files
    # no duplicates
    assert len(assigned) == len(files)

def test_slice_boundaries():
    files = list(range(10))
    shards = assign_shards(files, total_shards=3)
    # shard 0: 0-3, shard1: 3-6, shard2: 6-10
    assert shards[0] == [0, 1, 2, 3]
    assert shards[1] == [4, 5, 6]
    assert shards[2] == [7, 8, 9]

# test_projection.py
def test_parquet_stream_projection(tmp_path):
    path = tmp_path / "x.parquet"
    write_test_parquet(path, rows=[{"prompt": "p1", "response": "r1", "extra": "x"}, {"prompt": "p2", "response": "r2"}])
    out = list(stream_project(path))
    assert out == [{"prompt": "p1", "response": "r1"}, {"prompt": "p2", "response": "r2"}]

def test_jsonl_stream_projection_skips_malformed(tmp_path, capsys):
    path = tmp_path / "x.jsonl"
    path.write_text('{"prompt":"p1","response":"r1"}\nmalformed\n{"prompt":"p2","response":"r2"}\n')
    out = list(stream_project(path))
    assert out == [{"prompt": "p1", "response": "r1"}, {"prompt": "p2", "response": "r2"}]
    captured = capsys.readouterr()
    assert "warning" in captured.err.lower() or "skip" in captured.err.lower()

# test_download.py
def test_download_prefers_cdn_fallback(monkeypatch):
    cdn_called = []
    fallback_called = []
    monkeypatch.setattr("download.cdn_fetch", lambda u, dest: cdn_called.append((u, dest)) or exec('raise ConnectionError'))
    monkeypatch.setattr("download.hf_fallback", lambda r, f, dest: fallback_called.append((r, f, dest)) or Path(dest).write_text("ok"))
    download_file(repo_id="a/b", rel_path="x.parquet", dest="/tmp/x.parquet", use_cdn=True)
    assert len(cdn_called) == 1
    assert len(fallback_called) == 1
```

3. **Integration tests** (3 happy + 3 edge)

Happy paths
- Manifest-driven shard run (16 shards): pre-create `manifests/2024-
