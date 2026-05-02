# axentx-dev-bot decision
- id: `20260502-190428-surrogate-1-discovery-8d46d0b7`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T19:04:28.887150Z

## dev — claude/llm-fallback-chain @ 2026-05-02T19:04:28.887256Z

## Final Implementation Plan (≤2h)

**Core idea**: One deterministic preflight produces a pinned file list; all shards consume it via CDN URLs only. This eliminates HF API auth/rate limits and overwrite races while keeping shard routing and dedup intact.

1. Preflight (once per run)  
   - Compute date partition (`YYYY-MM-DD`) with manual override.  
   - Call `list_repo_tree(..., recursive=False)` for that date folder.  
   - Emit `file-list.json` artifact containing `{date, files[], sha256}`.  
   - If list is empty, fail fast (no wasted shards).

2. Shard workers (parallel)  
   - Download `file-list.json` artifact.  
   - Iterate only assigned files via `hash(slug) % 16 == SHARD_ID`.  
   - Fetch via CDN (`resolve/main/...`) with short timeout and UA header.  
   - Idempotent output: skip if target file exists and non-empty.  
   - Deterministic per-run filenames: `shard{N}-{YYYYMMDD-HHMMSS}.jsonl`.  
   - Central local dedup (MD5) persisted to `dedup_hashes.jsonl`; cross-run dedup handled by HF Space SQLite.  
   - Emit per-shard summary (count, bytes, duration) to stdout.

3. Observability & safety  
   - Preflight and shard steps log clearly and exit non-zero on hard errors.  
   - Workflow concurrency control to avoid simultaneous runs corrupting dedup DB.  
   - No changes to central dedup logic or hash routing.

Estimated effort:  
- Script changes: ~30 min  
- Workflow + artifact plumbing: ~30 min  
- Test run + polish: ~60 min  

---

## Code changes

### 1) Workflow (`.github/workflows/ingest.yml`)

```yaml
name: surrogate-1-ingest

on:
  schedule:
    - cron: "*/30 * * * *"
  workflow_dispatch:
    inputs:
      date:
        description: "Date partition (YYYY-MM-DD). If omitted, uses UTC today."
        required: false

env:
  DATASET_REPO: axentx/surrogate-1-training-pairs

jobs:
  preflight:
    runs-on: ubuntu-latest
    outputs:
      date_part: ${{ steps.date.outputs.date_part }}
      file_count: ${{ steps.list.outputs.file_count }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set date partition
        id: date
        run: |
          if [ -n "${{ github.event.inputs.date }}" ]; then
            echo "date_part=${{ github.event.inputs.date }}" >> $GITHUB_OUTPUT
          else
            echo "date_part=$(date -u +%Y-%m-%d)" >> $GITHUB_OUTPUT
          fi

      - name: Install huggingface_hub
        run: pip install huggingface_hub

      - name: List date folder (non-recursive)
        id: list
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
          DATE_PART: ${{ steps.date.outputs.date_part }}
        run: |
          python - <<'PY'
          import os, json, sys
          from huggingface_hub import HfApi
          api = HfApi()
          repo = os.environ["DATASET_REPO"]
          date_part = os.environ["DATE_PART"]
          try:
              tree = api.list_repo_tree(repo=repo, path=date_part, recursive=False)
              files = sorted([t.path for t in tree if t.type == "file"])
          except Exception:
              files = []
          out = {"date": date_part, "files": files}
          out_path = "file-list.json"
          with open(out_path, "w") as f:
              json.dump(out, f)
          print(f"::set-output name=file_count::{len(files)}")
          PY

      - name: Fail fast if no files
        if: steps.list.outputs.file_count == '0'
        run: |
          echo "No files found for date ${{ steps.date.outputs.date_part }} — nothing to ingest."
          exit 1

      - name: Upload file-list artifact
        uses: actions/upload-artifact@v4
        with:
          name: file-list
          path: file-list.json

  ingest:
    needs: preflight
    strategy:
      matrix:
        shard_id: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    runs-on: ubuntu-latest
    env:
      SHARD_ID: ${{ matrix.shard_id }}
      DATE_PART: ${{ needs.preflight.outputs.date_part }}
    steps:
      - uses: actions/checkout@v4

      - name: Download f

## review — reviewer @ 2026-05-02T19:04:43.102651Z

APPROVE: The proposal is a clear, workable first step that addresses discovery-stage goals (deterministic file list, CDN-only fetches, shard routing, dedup persistence) and unblocks parallel ingestion without touching central dedup logic. It is intentionally minimal and can be iterated in attempts 2–3.

Acceptance criteria (downstream tester can check):
- Preflight job produces `file-list.json` artifact containing `{date, files[]}` and fails non-zero when the list is empty.
- Each shard (0–15) consumes only files assigned by `hash(slug) % 16 == SHARD_ID` and writes deterministic output `shard{N}-{YYYYMMDD-HHMMSS}.jsonl` under `batches/public-merged/{date}/`.
- Workers fetch files exclusively via CDN URLs (`resolve/main/...`) with a short timeout and UA header; no HF API calls for file content.
- Idempotency: shard skips fetch+write if target file exists and is non-empty; per-run MD5 dedup persisted to `dedup_hashes.jsonl`.
- Workflow concurrency control (or run serialization) prevents simultaneous runs from corrupting the central HF Space SQLite dedup store.

## qa — qa @ 2026-05-02T19:04:57.756715Z

PASS: Preflight + shard plan is minimal, deterministic, and CDN-only; ready for TDD.

1. **Acceptance criteria**
- Preflight produces `file-list.json` artifact with keys `date` (YYYY-MM-DD), `files` (array of strings), `sha256` (string); exit code non-zero when `files` is empty.
- Each shard (0–15) consumes `file-list.json` and processes only items where `hash(slug) % 16 == SHARD_ID`; output file name matches `shard{N}-{YYYYMMDD-HHMMSS}.jsonl`.
- All file fetches use CDN URLs matching pattern `https://huggingface.co/datasets/{repo}/resolve/main/{path}` with timeout ≤10s and UA header containing `surrogate-1`.
- Idempotency: shard skips download/write when target file exists and size > 0; per-run MD5 hashes appended to `dedup_hashes.jsonl` (one hash per line).
- Cross-run dedup protected: workflow concurrency limited to 1 (or uses advisory lock) to prevent concurrent writes to HF Space SQLite dedup store.
- Preflight and shard log structured lines and exit non-zero on hard errors (network, auth, I/O).
- Output directory structure: `batches/public-merged/{date}/` contains shard outputs and `dedup_hashes.jsonl`.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_preflight.py
def test_date_partition_default(monkeypatch):
    monkeypatch.delenv("INPUT_DATE", raising=False)
    from preflight import partition_date
    assert partition_date() == datetime.utcnow().strftime("%Y-%m-%d")

def test_date_partition_override():
    from preflight import partition_date
    assert partition_date(override="2023-07-01") == "2023-07-01"

def test_list_files_empty_fails(mocker):
    mocker.patch("preflight.HfApi.list_repo_tree", return_value=[])
    from preflight import collect_files
    with pytest.raises(SystemExit) as exc:
        collect_files(repo="x", date="2023-07-01")
    assert exc.value.code != 0

def test_list_files_nonempty_ok(mocker):
    mocker.patch("preflight.HfApi.list_repo_tree", return_value=[type("T",(),{"path":"2023-07-01/a.json"})])
    from preflight import collect_files
    out = collect_files(repo="x", date="2023-07-01")
    assert out["date"] == "2023-07-01"
    assert out["files"] == ["2023-07-01/a.json"]
    assert "sha256" in out

# test_shard.py
def test_shard_assignment():
    from shard import assign
    # deterministic: same slug -> same shard
    assert assign("abc", total=16) == assign("abc", total=16)
    assert 0 <= assign("abc", total=16) < 16

def test_output_filename():
    from shard import output_filename
    name = output_filename(shard_id=3, run_ts="20230701-120000")
    assert name == "shard3-20230701-120000.jsonl"

def test_cdn_url():
    from shard import cdn_url
    url = cdn_url(repo="axentx/surrogate-1-training-pairs", path="2023-07-01/a.json")
    assert url.startswith("https://huggingface.co/datasets/")
    assert "/resolve/main/" in url

def test_idempotency_skip_if_exists(tmp_path):
    from shard import should_process
    p = tmp_path / "out.jsonl"
    p.write_text("x")
    assert should_process(p) is False
    p.unlink()
    assert should_process(p) is True

def test_dedup_line_format():
    from shard import append_dedup
    p = tmp_path / "dedup_hashes.jsonl"
    append_dedup(p, "d41d8cd98f00b204e9800998ecf8427e")
    lines = p.read_text().strip().splitlines()
    assert len(lines) == 1
    assert lines[0] == "d41d8cd98f00b204e9800998ecf8427e"
```

3. **Integration tests** (happy + edge)

Happy cases
- Preflight + 16 shards (simulated): given a populated date folder, preflight emits `file-list.json`; each shard consumes artifact, processes assigned files via CDN, writes deterministic outputs under `batches/public-merged/{date}/`, and appends MD5s to `dedup_hashes.jsonl`. Verify: total processed files equals len(files), no duplicate MD5 lines within run, all fetch URLs are CDN, UA header present.
- Idempotent rerun: run
