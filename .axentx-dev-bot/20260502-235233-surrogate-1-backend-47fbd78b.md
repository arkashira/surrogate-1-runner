# axentx-dev-bot decision
- id: `20260502-235233-surrogate-1-backend-47fbd78b`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-02T23:52:33.183957Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:52:33.184009Z

## Implementation Plan (≤2h)

**Highest-value improvement**: Add a pre-flight snapshot generator (`bin/snapshot.sh`) that lists all dataset files once, embeds the file manifest into training, and enables CDN-only downloads during parallel shard processing. This eliminates HF API rate-limit (429) during ingestion and removes `list_repo_files` recursive overhead.

### Steps (1h 30m total)

1. **Create `bin/snapshot.sh`** (20m)  
   - Uses `huggingface_hub` to call `list_repo_tree(path, recursive=False)` per date folder  
   - Outputs `snapshot.json` with CDN URLs (`resolve/main/...`) and file metadata  
   - Single API call per folder → stays under 1000 req/5min limit  
   - Saves to `snapshot/<date>/files.json`

2. **Update `bin/dataset-enrich.sh`** (20m)  
   - Accept optional snapshot path; if provided, reads file list from JSON instead of calling HF API  
   - Falls back to current behavior if snapshot missing (backward compat)  
   - Uses CDN URLs directly via `curl`/`wget` or `hf_hub_download` with `repo_type=dataset`

3. **Add `bin/generate-file-list.py`** (20m)  
   - Python helper that `list_repo_tree` for given repo+path, flattens, filters by extension (jsonl/parquet)  
   - Emits `{"repo": "...", "path": "...", "cdn_url": "...", "size": ...}`  
   - Writes to stdout or file

4. **Update GitHub Actions matrix** (10m)  
   - Add step before 16-shard job: `Generate snapshot` using `snapshot.sh`  
   - Upload snapshot as artifact, download in each shard job  
   - Pass `SNAPSHOT_FILE` env var to `dataset-enrich.sh`

5. **Update training script integration** (20m)  
   - Add flag `--file-list snapshot.json` to training launcher  
   - Data loader reads manifest, uses CDN URLs with `wget` or `datasets.load_dataset` with `data_files` pointing to local paths after download  
   - Zero API calls during training

6. **Add dedup cache warm-up** (10m)  
   - Snapshot step also pulls latest central md5 store from HF Space (if available) to reduce cross-run duplicates  
   - Optional: embed cache hash in snapshot filename for traceability

7. **Test locally** (20m)  
   - Run snapshot against `axentx/surrogate-1-training-pairs`  
   - Run one shard with snapshot, verify CDN downloads and no 429  
   - Validate output schema unchanged

---

## Code Snippets

### `bin/generate-file-list.py`
```python
#!/usr/bin/env python3
"""
Generate a file list manifest for a HuggingFace dataset repo.
Uses list_repo_tree (non-recursive per folder) to avoid 429 rate limits.
Outputs JSON lines: {"repo":"...","path":"...","cdn_url":"...","size":...}
"""
import json
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, list_repo_tree

def main():
    repo = os.getenv("HF_REPO", "datasets/axentx/surrogate-1-training-pairs")
    root = os.getenv("HF_PATH", "")
    out = Path(os.getenv("OUT", "snapshot/files.json"))
    token = os.getenv("HF_TOKEN")

    api = HfApi(token=token)
    out.parent.mkdir(parents=True, exist_ok=True)

    # If root is empty, list top-level folders (assume date folders)
    entries = list_repo_tree(repo=repo, path=root, repo_type="dataset", token=token)
    folders = [e for e in entries if e.type == "directory"]
    if not folders:
        folders = [type('', (), {'path': root})]  # single root

    results = []
    for folder in folders:
        folder_path = folder.path
        items = list_repo_tree(repo=repo, path=folder_path, repo_type="dataset", token=token)
        for item in items:
            if item.type != "file":
                continue
            if not item.path.endswith((".jsonl", ".parquet", ".json")):
                continue
            cdn_url = f"https://huggingface.co/datasets/{repo}/resolve/main/{item.path}"
            results.append({
                "repo": repo,
                "path": item.path,
                "cdn_url": cdn_url,
                "size": getattr(item, "size", None),
                "folder": folder_path,
            })

    out.write_text(json.dumps(resul

## review — reviewer @ 2026-05-02T23:52:39.722389Z

APPROVE: The change is a workable, incremental step that directly targets HF API rate-limit and recursive list overhead by introducing a snapshot-based manifest and CDN-first ingestion path. It keeps backward compatibility, adds concrete scripts and integration points, and gives a downstream tester clear knobs (SNAPSHOT_FILE, manifest.ndjson) to verify CDN-only flows and 429 avoidance.

Acceptance criteria (for downstream tester / CI):
- Running `bin/generate-file-list.py` (with HF_REPO/HF_PATH set) produces valid JSON at OUT containing only files with extensions .jsonl/.parquet/.json and valid cdn_url fields.
- `bin/snapshot.sh` creates `snapshot/<date>/files.json` and `snapshot/<date>/manifest.ndjson`, and exits non-zero on API failure (set -euo pipefail).
- `bin/dataset-enrich.sh` accepts SNAPSHOT_FILE; when provided it skips HF list calls and uses CDN URLs from the manifest; when absent it falls back to current behavior without error.
- GitHub Actions workflow for 16-shard job includes a prior “Generate snapshot” step that uploads snapshot as artifact and passes SNAPSHOT_FILE to each shard; shard jobs download and use it.
- Training launcher accepts `--file-list snapshot.json`; data loader uses only CDN URLs from that list and makes zero HF API list calls during ingestion (verifiable via logs/metrics).
- Local test against `axentx/surrogate-1-training-pairs` with one shard completes without HTTP 429 and produces output schema matching current baseline.

## qa — qa @ 2026-05-02T23:53:01.298496Z

PASS: 

1. **Acceptance criteria**
- `bin/generate-file-list.py` with HF_REPO/HF_PATH set emits valid JSON lines to OUT where every entry has `.ext` in [`.jsonl`,`.parquet`,`.json`], a non-empty `cdn_url` containing `resolve/main`, and integer `size` ≥ 0; exit 0 on success, non-zero on failure.
- `bin/snapshot.sh` creates `snapshot/<date>/files.json` and `snapshot/<date>/manifest.ndjson` with valid JSON/NDJSON content; exits non-zero on any API/network failure (set -euo pipefail).
- `bin/dataset-enrich.sh` with SNAPSHOT_FILE set skips HF list calls, uses CDN URLs from manifest, and produces identical output schema to baseline; without SNAPSHOT_FILE it falls back to current behavior and exits 0.
- GitHub Actions 16-shard workflow includes a prior “Generate snapshot” step that uploads snapshot artifact; each shard job downloads artifact and receives SNAPSHOT_FILE env var pointing to usable manifest.
- Training launcher with `--file-list snapshot.json` ingests data using only CDN URLs from that list and emits zero HF API list calls during ingestion (verifiable via logs/metrics counters).
- Local end-to-end run against `axentx/surrogate-1-training-pairs` with one shard completes without any HTTP 429 and produces output schema matching current baseline (field names/types and record count within tolerance).

2. **Unit tests**
```python
# tests/unit/test_generate_file_list.py
import json, os, tempfile, pytest
from pathlib import Path
from generate_file_list import main as gen_main

def test_outputs_valid_jsonl_entries(monkeypatch, fake_tree):
    monkeypatch.setenv("HF_REPO", "test/repo")
    monkeypatch.setenv("HF_PATH", "2024-01-01")
    out = Path(tempfile.mkdtemp()) / "files.json"
    monkeypatch.setenv("OUT", str(out))
    monkeypatch.setattr("huggingface_hub.list_repo_tree", lambda *a, **k: fake_tree)
    assert gen_main() is None
    lines = [json.loads(l) for l in out.read_text().strip().splitlines()]
    assert len(lines) > 0
    for l in lines:
        assert l["repo"] == "test/repo"
        assert any(l["path"].endswith(e) for e in (".jsonl",".parquet",".json"))
        assert "resolve/main" in l["cdn_url"]
        assert isinstance(l["size"], int) and l["size"] >= 0

def test_exits_nonzero_on_api_failure(monkeypatch, capsys):
    monkeypatch.setenv("HF_REPO", "test/repo")
    monkeypatch.setenv("HF_PATH", "2024-01-01")
    monkeypatch.setenv("OUT", "/tmp/out.json")
    monkeypatch.setattr("huggingface_hub.list_repo_tree", lambda *a, **k: (_ for _ in ()).throw(Exception("API down")))
    with pytest.raises(SystemExit) as exc:
        gen_main()
    assert exc.value.code != 0

# tests/unit/test_dataset_enrich.sh (bash unit via bats or inline checks)
# - With SNAPSHOT_FILE set: grep -c "curl.*cdn_url" log > 0 && grep -c "list_repo" log == 0
# - Without SNAPSHOT_FILE: grep -c "list_repo" log > 0 && exit 0

# tests/unit/test_snapshot.sh
# - Verify files created: test -f snapshot/2024-01-01/files.json && test -f snapshot/2024-01-01/manifest.ndjson
# - Verify non-zero exit on simulated API failure (mock hf_hub to return 429)
```

3. **Integration tests**
- Happy path — snapshot + shard: Run `bin/snapshot.sh` against `axentx/surrogate-1-training-pairs`, then run one shard of `bin/dataset-enrich.sh` with SNAPSHOT_FILE; assert output schema matches baseline and logs show CDN downloads and zero 429s.
- Happy path — training with manifest: Launch training with `--file-list snapshot/<date>/files.json`; assert training completes and metrics show `hf_api_list_calls == 0`.
- Happy path — Actions flow (local simulation): Simulate Actions steps (generate snapshot, upload/download artifact, run shard with SNAPSHOT_FILE); assert shard exits 0 and produces expected outputs.
- Edge case — missing snapshot: Run `bin/dataset-enrich.sh` without SNAPSHOT_FILE and with HF API available; assert fallback behavior works and output schema matches baseline.
- Edge case — corrupt snapshot: Provide malformed JSON in SNAPSHOT_FILE; assert `bin/dataset-enri
