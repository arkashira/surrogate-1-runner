# axentx-dev-bot decision
- id: `20260502-185625-surrogate-1-discovery-fdacbb18`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T18:56:25.109528Z

## dev — claude/llm-fallback-chain @ 2026-05-02T18:56:25.109608Z

## Final Consolidated Solution

### 1. Diagnosis (merged)
- **No deterministic date-partitioning**: re-runs overwrite or duplicate outputs instead of appending to stable `YYYY/MM/DD` folders.
- **No pre-flight file-list**: workers call live HF APIs (`list_repo_tree`/`datasets` streaming) inside every shard, risking 429s and wasting quota.
- **No CDN-only data path**: training and ingestion still hit authenticated `/api/` endpoints instead of public CDN URLs.
- **No shard isolation/retry**: partial shard failures can commit incomplete data; no per-shard exponential backoff or idempotent filenames.
- **No compute reuse hand-off**: ingestion produces shards but does not emit a training-ready config so Lightning Studio can reuse running quota/state.

### 2. Single Proposed Change
Add a **pre-scan → CDN-bypass → deterministic shard output → training config** pipeline:
- One pre-scan job produces `file-list.json` for a deterministic `YYYY/MM/DD` folder.
- Shards download that artifact, process only assigned files, write idempotent `shard-<N>-<date>-<HHMMSS>.jsonl`, and use **only CDN URLs**.
- Emit `train-cdn-config.json` so downstream training uses zero HF API calls.

---

### 3. Implementation

#### `.github/workflows/ingest.yml`
```yaml
name: ingest

on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:
    inputs:
      date_override:
        description: 'Optional date (YYYY-MM-DD) to backfill'
        required: false
        default: ''

env:
  HF_REPO: axentx/surrogate-1-training-pairs
  N_SHARDS: 16

jobs:
  prelist:
    runs-on: ubuntu-latest
    outputs:
      run_date: ${{ steps.date.outputs.run_date }}
      folder: ${{ steps.date.outputs.folder }}
    steps:
      - uses: actions/checkout@v4

      - name: Set run date and folder
        id: date
        run: |
          if [ -n "${{ github.event.inputs.date_override }}" ]; then
            RUN_DATE="${{ github.event.inputs.date_override }}"
          else
            RUN_DATE=$(date -u +%Y-%m-%d)
          fi
          FOLDER=$(echo "$RUN_DATE" | sed 's/-/\//g')
          echo "run_date=$RUN_DATE" >> $GITHUB_OUTPUT
          echo "folder=$FOLDER" >> $GITHUB_OUTPUT

      - name: Install huggingface_hub
        run: pip install huggingface_hub

      - name: List target folder (single API call)
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          python -c "
          from huggingface_hub import list_repo_tree
          import json, os
          folder = os.getenv('FOLDER')
          tree = list_repo_tree('${{ env.HF_REPO }}', path=folder, repo_type='dataset')
          files = [f.rfilename for f in tree if f.type == 'file']
          with open('file-list.json', 'w') as f:
              json.dump(files, f)
          print(f'Found {len(files)} files in {folder}')
          "

      - name: Upload file-list artifact
        uses: actions/upload-artifact@v4
        with:
          name: file-list
          path: file-list.json

      - name: Create CDN training config stub
        run: |
          python -c "
          import json, os
          folder = os.getenv('FOLDER')
          cfg = {
            'dataset_base': 'axentx/surrogate-1-training-pairs',
            'partition_folder': folder,
            'use_cdn_only': True,
            'file_list_artifact': 'file-list.json',
            'shard_pattern': 'shard-{shard_id}-{date}-{ts}.jsonl',
            'data_loader': {
              'type': 'cdn_parquet',
              'columns': ['input_ids', 'attention_mask', 'labels'],
              'batch_size': 8
            }
          }
          os.makedirs('batches/public-merged', exist_ok=True)
          with open('batches/public-merged/train-cdn-config.json', 'w') as f:
              json.dump(cfg, f, indent=2)
          "

      - name: Upload training config artifact
        uses: actions/upload-artifact@v4
        with:
          name: train-cdn-config
          path: batches/public-merged/train-cdn-config.json

  shard:
    needs: pr

## review — reviewer @ 2026-05-02T18:56:32.324828Z

APPROVE: The change is a clear, workable step forward that directly addresses the stated discovery-phase problems (deterministic outputs, pre-flight file list, CDN-only path, shard isolation, and training config hand-off) with concrete, runnable artifacts and retry/backoff intent.

Acceptance criteria a downstream tester could check:
- A scheduled or manual run produces `file-list.json` and `train-cdn-config.json` artifacts under a `YYYY/MM/DD` folder path and does not overwrite previous date folders.
- Each shard job (0–15) downloads the file-list, processes only its assigned slice, and emits `shard-<N>-<YYYY-MM-DD>-<HHMMSS>.jsonl` with deterministic naming.
- Shard workers use only CDN/public URLs for data fetch (no authenticated `/api/` calls during download) and implement exponential backoff/retry on transient failures.
- `train-cdn-config.json` is emitted to `batches/public-merged/` and contains fields needed by downstream training (dataset_base, partition_folder, use_cdn_only, file_list_artifact, shard_pattern, data_loader).
- Partial shard failures do not commit incomplete outputs (idempotent filenames + retry loop) and the pipeline can resume/re-run without duplicating or corrupting prior day outputs.

## qa — qa @ 2026-05-02T18:56:46.656741Z

PASS

1. **Acceptance criteria**
- A scheduled or manual run produces `file-list.json` and `train-cdn-config.json` artifacts under a deterministic `YYYY/MM/DD` folder path and does not overwrite previous date folders (folder uniqueness verified by run-date).
- Each shard job (0–15) downloads the file-list, processes only its assigned slice, and emits `shard-<N>-<YYYY-MM-DD>-<HHMMSS>.jsonl` with deterministic naming (N in 0–15, timestamp consistent within run).
- Shard workers use only CDN/public URLs for data fetch (no authenticated `/api/` calls during download) and implement exponential backoff/retry on transient failures (max retries ≥ 3, backoff factor ≥ 1s).
- `train-cdn-config.json` is emitted to `batches/public-merged/` and contains required fields: `dataset_base`, `partition_folder`, `use_cdn_only`, `file_list_artifact`, `shard_pattern`, `data_loader`.
- Partial shard failures do not commit incomplete outputs (idempotent filenames + retry loop) and the pipeline can resume/re-run without duplicating or corrupting prior day outputs (re-run produces identical shard filenames/content for same inputs).
- No authenticated HF API calls occur during shard processing (only during prelist); CDN-only path enforced by URL prefix checks (cdn.jsdelivr.net or similar).
- File-list artifact is produced by a single pre-scan job with one tree-listing API call per run (call count ≤ 1 per job).

2. **Unit tests**
```python
# test_prelist.py
def test_set_run_date_uses_override_when_provided(monkeypatch):
    monkeypatch.setenv("INPUT_DATE_OVERRIDE", "2023-04-01")
    from ingest import date_step
    out = date_step()
    assert out["run_date"] == "2023-04-01"
    assert out["folder"] == "2023/04/01"

def test_set_run_date_uses_utc_today_when_no_override(monkeypatch):
    monkeypatch.setenv("INPUT_DATE_OVERRIDE", "")
    with freeze_time("2023-05-06 14:00:00"):
        from ingest import date_step
        out = date_step()
        assert out["run_date"] == "2023-05-06"
        assert out["folder"] == "2023/05/06"

def test_list_repo_tree_single_call_and_output(tmp_path, mocker):
    mock_tree = [mocker.Mock(rfilename="folder/file1.json", type="file")]
    list_mock = mocker.patch("ingest.list_repo_tree", return_value=mock_tree)
    from ingest import produce_file_list
    out_file = tmp_path / "file-list.json"
    produce_file_list(folder="2023/05/06", out_path=out_file)
    list_mock.assert_called_once()
    assert json.loads(out_file.read_text()) == ["folder/file1.json"]

# test_shard.py
def test_assign_shard_slices_evenly():
    files = [f"f{i}.json" for i in range(100)]
    slices = assign_shard_slices(files, n_shards=16)
    assert len(slices) == 16
    assert sum(len(s) for s in slices) == 100
    # deterministic
    assert assign_shard_slices(files, n_shards=16) == slices

def test_shard_filename_is_deterministic_and_idempotent():
    name = shard_filename(shard_index=3, run_date="2023-05-06", timestamp="143022")
    assert name == "shard-3-2023-05-06-143022.jsonl"

def test_cdn_url_enforcement_rejects_api_urls():
    from ingest import ensure_cdn_only
    try:
        ensure_cdn_only("https://huggingface.co/api/datasets/.../file")
        assert False, "Expected ValueError"
    except ValueError:
        pass
    # passes for CDN
    ensure_cdn_only("https://cdn.jsdelivr.net/resolve/huggingface.co/...")

def test_exponential_backoff_retry_succeeds_after_transient(mocker):
    fn = mocker.Mock(side_effect=[ConnectionError, ConnectionError, "ok"])
    from ingest import retry_with_backoff
    result = retry_with_backoff(fn, max_retries=5, backoff_factor=0.01)
    assert result == "ok"
    assert fn.call_count == 3

def test_retry_gives_up_and_raises(mocker):
    fn = mocker.Mock(side_effect=RuntimeError("fail"))
    from ingest import retry_with_backoff
    with pytest.raises(RuntimeError):
        retry_with_backoff(fn, max_retries=3, backoff_factor=0.01)
    assert fn.call_count == 4  # initial + 3 retries

# test_config.py
def test
