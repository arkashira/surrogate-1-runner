# axentx-dev-bot decision
- id: `20260502-185840-surrogate-1-discovery-9ca4269a`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T18:58:40.871691Z

## dev — claude/llm-fallback-chain @ 2026-05-02T18:58:40.871792Z

**Final synthesized plan (highest correctness + concrete actionability)**

- **Deterministic date-partitioned output**  
  Use UTC run date `YYYY/MM/DD` in the path so re-runs append instead of overwrite and training data history is stable.

- **Single pre-flight file list + CDN-only fetches**  
  Generate `file-list.json` once per workflow (not per shard) via `list_repo_tree` for the target date folder; workers download this artifact and stream files directly from CDN (`resolve/main/...`). This removes repeated HF API calls, avoids auth/rate-limit issues, and guarantees all shards see the same snapshot.

- **Deterministic, disjoint shard assignment**  
  Each worker hashes `relpath` (e.g., MD4/MD5 truncated) modulo 16 and processes only files assigned to its `SHARD_ID`. This is stable across runs and removes redundant work.

- **Schema/traceability + robustness**  
  Emit `source_file`, `ingest_ts` (and keep any existing `prompt`/`response` schema). Add retries with jitter for CDN downloads, strict bash hygiene (`#!/usr/bin/env bash`, `set -euo pipefail`), and fast-fail if `SHARD_ID` is invalid.

- **Dedup**  
  Keep existing `lib/dedup.py` (central md5 store) for cross-run dedup; workers can skip persisting records whose hashes are already known to reduce wasted writes.

---

**Implementation plan (concrete, ≤2h)**

1. **Workflow changes** (`.github/workflows/ingest.yml`)
   - Compute `RUN_DATE` and `PARTITION` (YYYY/MM/DD) once.
   - Add a pre-flight step that lists the target `PARTITION` folder (non-recursive) via `huggingface_hub.HfApi.list_repo_tree`, writes `file-list.json`, and uploads it as an artifact.
   - Matrix job for 16 shards, passing `SHARD_ID`, `RUN_DATE`, `PARTITION`, and making the artifact available to all shards.

2. **Worker script** (`bin/dataset-enrich.sh`)
   - Validate `SHARD_ID` in 0..15 and required env.
   - Download `file-list.json` artifact (or use local if present).
   - Deterministic shard assignment: `hash(relpath) % 16 == SHARD_ID`.
   - For each assigned file:
     - Build CDN URL: `https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/<relpath>`.
     - Download with retries (3×, exponential/jitter) and stream-parse to `{prompt, response, source_file, ingest_ts}`.
     - Skip if dedup store already contains hash (optional per-worker fast skip).
     - Append to `batches/public-merged/${PARTITION}/shard${SHARD_ID}-${RUN_DATE}-${HHMMSS}.jsonl`.
   - Use `#!/usr/bin/env bash`, `set -euo pipefail`, `chmod +x`.

3. **Dedup** (`lib/dedup.py`)
   - No functional change; continue using central md5 store. Workers may call it to check/insert hashes.

---

**Code snippets**

`.github/workflows/ingest.yml` (excerpt)
```yaml
env:
  RUN_DATE: ${{ steps.date.outputs.run_date }}
  PARTITION: ${{ steps.date.outputs.partition }}

steps:
  - name: Compute date partition
    id: date
    run: |
      echo "run_date=$(date -u +%Y-%m-%d)" >> $GITHUB_OUTPUT
      echo "partition=$(date -u +%Y/%m/%d)" >> $GITHUB_OUTPUT

  - name: Generate file-list (once per workflow)
    id: filelist
    run: |
      python - <<'PY'
      import os, json
      from huggingface_hub import HfApi
      api = HfApi()
      repo = "axentx/surrogate-1-training-pairs"
      partition = os.getenv("PARTITION")
      items = api.list_repo_tree(repo, path=partition, recursive=False)
      files = [i.rfilename for i in items if i.type == "file"]
      with open("file-list.json", "w") as f:
          json.dump(files, f)
      print(f"Listed {len(files)} files for {partition}")
      PY

  - name: Upload file-list artifact
    uses: actions/upload-artifact@v4
    with:
      name: file-list-${{ env.PARTITION }}
      path: file-list.json

  - name: Run shards
    uses: matrix-job
    with:
      matrix: '{"shard": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]}'
    env:
      SHARD_ID: ${{ matrix.shard }}
      RUN_DATE: ${{ env.RUN_DATE }}
      PARTITION: ${{ env.PARTITION }}
```

`bin/dataset-enrich.sh`
```bash
#!/usr/bi

## review — reviewer @ 2026-05-02T18:58:57.169356Z

APPROVE: Deterministic partitioning, single file-list artifact, stable shard assignment, and CDN-only fetches are a clear, workable step forward that removes overwrite races and HF API hammering while giving downstream testers concrete acceptance criteria.

Acceptance criteria (for testers/verification):
- Workflow produces `file-list.json` artifact containing only files under `PARTITION` (YYYY/MM/DD) and matrix runs 16 shards with `SHARD_ID=0..15`.
- Each worker emits to `batches/public-merged/<PARTITION>/shard<N>-<RUN_DATE>-<HHMMSS>.jsonl` and never writes outside its assigned shard (hash(relpath) % 16 == SHARD_ID).
- Re-runs on the same UTC day append new timestamped files without overwriting prior day’s outputs (path includes `PARTITION` and timestamp).
- Workers use CDN URLs (`resolve/main/<relpath>`) and implement retries with jitter; no direct HF API calls per file during shard processing.
- Script fails fast on invalid `SHARD_ID` or missing `file-list.json`, and uses `#!/usr/bin/env bash` + `set -euo pipefail`.

## qa — qa @ 2026-05-02T18:59:11.919337Z

PASS: deterministic partitioning, single file-list artifact, stable shard assignment, CDN-only fetches, and dedup integration are testable and safe to proceed.

1. **Acceptance criteria**
- Workflow produces `file-list.json` containing only files under `PARTITION` (YYYY/MM/DD) and the matrix runs exactly 16 shards with `SHARD_ID=0..15`.
- Each worker emits to `batches/public-merged/<PARTITION>/shard<N>-<RUN_DATE>-<HHMMSS>.jsonl` and never writes records outside its assigned shard (hash(relpath) % 16 == SHARD_ID).
- Re-runs on the same UTC day append new timestamped files without overwriting prior outputs; path includes `PARTITION` and timestamp.
- Workers use CDN URLs (`https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/<relpath>`) and implement retries with jitter; zero per-file HF API calls during shard processing.
- Script fails fast on invalid `SHARD_ID` (not 0..15) or missing `file-list.json` with non-zero exit code.
- All emitted records include `source_file` and `ingest_ts` fields in addition to existing `prompt`/`response` schema.
- Dedup store is consulted per record; records with known md5 hashes are skipped (no duplicate writes).

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_shard_assignment.py
def test_hash_mod_stable():
    relpath = "2024/06/01/file-001.jsonl"
    assert shard_for(relpath, total=16) == hashlib.md5(relpath.encode()).digest()[0] % 16

def test_all_shards_covered():
    relpaths = [f"2024/06/01/file-{i:03}.jsonl" for i in range(1000)]
    assigned = {shard_for(r, 16) for r in relpaths}
    assert assigned == set(range(16))

# test_validation.py
def test_rejects_invalid_shard_id():
    with pytest.raises(SystemExit, match="SHARD_ID"):
        validate_env({"SHARD_ID": "16", "PARTITION": "2024/06/01", "RUN_DATE": "2024-06-01"})

def test_rejects_missing_file_list(tmp_path):
    with pytest.raises(SystemExit, match="file-list.json"):
        run_worker(shard_id=0, file_list_path=tmp_path / "missing.json")

# test_cdn_url.py
def test_build_cdn_url():
    assert build_cdn_url("2024/06/01/file.jsonl") == \
        "https://huggingface.co/datasets/axentx/surrogate-1-training-pairs/resolve/main/2024/06/01/file.jsonl"

# test_schema.py
def test_emitted_record_has_required_fields():
    record = process_record({"prompt": "p", "response": "r"}, relpath="a/b.jsonl")
    assert {"prompt", "response", "source_file", "ingest_ts"} <= set(record.keys())
    assert record["source_file"] == "a/b.jsonl"
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", record["ingest_ts"])

# test_dedup.py
def test_skip_known_hash(tmp_path, monkeypatch):
    store = DedupStore(tmp_path / "md5.db")
    h = "abcd" * 8
    store.insert(h)
    monkeypatch.setattr("lib.dedup.DedupStore.lookup", lambda self, x: store.lookup(x))
    assert should_skip(h, dedup=store) is True
```

3. **Integration tests** (happy + edge)

Happy paths
- Happy 1 — End-to-end single shard: workflow generates `file-list.json` for `2024/06/01`; worker with `SHARD_ID=3` downloads artifact, streams assigned files via CDN, emits `batches/public-merged/2024/06/01/shard3-2024-06-01-*.jsonl`; all records have correct schema and shard assignment.
- Happy 2 — 16-shard matrix completeness: run matrix for 16 shards against a fixture tree; union of outputs contains every file from `file-list.json` exactly once (no missing/duplicate assignments).
- Happy 3 — Re-run idempotency and append: run same partition twice; second run produces new timestamped file and does not overwrite first; total record count equals sum of both runs and no data loss.

Edge cases
- Edge 1 — Empty partition: `file-list.json` is empty array; workers exit cleanly with zero output files and zero errors.
- Edge 2 — CDN transient failure then success: simulate 500/timeout on first two CDN attempts; retry-with-jitter succeeds and record is emitted; verify no duplicate insert after retry.
- Edge 3 — Known hash in dedup store: worker skips writing record w
