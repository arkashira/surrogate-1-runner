# axentx-dev-bot decision
- id: `20260503-011619-surrogate-1-backend-1ea3bd97`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-03T01:16:19.641245Z

## dev — claude/llm-fallback-chain @ 2026-05-03T01:16:19.641321Z

## Final Decision — highest-value <2h backend fix
**Replace recursive HF API ingestion and per-file authenticated fetches with a single non-recursive `list_repo_tree` per date folder + CDN-bypass ingestion + pre-listed manifest.**  
- Eliminates recursive pagination (primary 429 source).  
- Eliminates per-file authenticated API calls during ingestion (rate-limit and commit-cap pressure).  
- Keeps ingestion deterministic, shard-safe, and backwards-compatible.

---

## Implementation plan (≤2h)

1. **Add `bin/list-folder-manifest.sh`**  
   - Accepts `REPO`, `FOLDER`, `OUT_JSON`.  
   - Calls `huggingface_hub.list_repo_tree(path=FOLDER, recursive=False)` once.  
   - Emits compact manifest:  
     ```json
     {
       "repo": "...",
       "folder": "...",
       "ts": "...",
       "files": [
         {"path": "...", "sha": "...", "size": ...},
         ...
       ]
     }
     ```
   - Idempotent: exits 0 with empty `files` if folder missing.

2. **Update `bin/dataset-enrich.sh`**  
   - Accept optional `MANIFEST_FILE`.  
   - If manifest present and valid, skip all listing; iterate only files in manifest.  
   - If manifest absent/invalid, run `list-folder-manifest.sh` once per job (not per file).  
   - Download each file via **CDN URL** (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) with curl (no auth header).  
   - Fallback to authenticated `hf_hub_download` on CDN 404 (future-proof for private repos).  
   - Keep existing schema projection, md5 dedup (`lib/dedup.py`), and shard upload.  
   - Upload to deterministic path:  
     `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl`

3. **Add `lib/file_io.py` helpers**  
   - `download_via_cdn(repo, path, dest)` with curl + authenticated fallback.  
   - `project_to_pair(file_path)` isolates schema normalization for parquet/jsonl into `{prompt, response}`.

4. **GitHub Actions hygiene (optional but recommended)**  
   - Add a pre-matrix step to generate the manifest for the current date folder and upload as artifact.  
   - Each shard job downloads the same artifact → zero per-shard API list calls → eliminates 429 during ingestion window.

5. **Cron / scheduling hygiene**  
   - Ensure `SHELL=/bin/bash` in crontab entries and `#!/usr/bin/env bash` + `chmod +x` on all bin scripts.

6. **Smoke test**  
   - Run `bin/list-folder-manifest.sh` locally or via GH Actions dry-run.  
   - Run a single shard with `MANIFEST_FILE=manifest-YYYY-MM-DD.json bin/dataset-enrich.sh`.  
   - Verify output file in repo and confirm no 429/403 in logs.

---

## Code snippets

### bin/list-folder-manifest.sh
```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="${HF_REPO:-axentx/surrogate-1-training-pairs}"
FOLDER="${1:-public-merged/$(date +%Y-%m-%d)}"
OUT="${2:-manifest-$(date +%Y-%m-%d).json}"

python3 - "$REPO" "$FOLDER" "$OUT" <<'PY'
import json
import sys
from datetime import datetime, timezone
from huggingface_hub import HfApi

repo = sys.argv[1]
folder = sys.argv[2]
out = sys.argv[3]

api = HfApi()
files = []
try:
    tree = api.list_repo_tree(repo=repo, path=folder, recursive=False)
    for node in tree:
        files.append({
            "path": node.path,
            "sha": getattr(node, "sha", None),
            "size": getattr(node, "size", None),
        })
except Exception as e:
    # folder may not exist yet — treat as empty
    print(f"Warning: {e}", file=sys.stderr)

manifest = {
    "repo": repo,
    "folder": folder,
    "ts": datetime.now(timezone.utc).isoformat(),
    "files": files,
}

with open(out, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"Wrote {len(files)} entries to {out}")
PY
```

### lib/file_io.py
```python
import os
import json
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from huggingface_hub import hf_hub_download

CDN_TEMPLATE = "https://huggingface.co/datasets/{repo}/resolve/main/{path}"

def download_via_cdn(repo: str, path: str, dest: Path) -> str:
   

## review — reviewer @ 2026-05-03T01:16:27.049089Z

APPROVE: The change is a clear, workable step forward — it replaces recursive/authenticated ingestion with a single non-recursive tree listing + CDN downloads, directly targeting the 429/rate-limit problem while keeping ingestion deterministic and shard-safe.

Acceptance criteria:
- `bin/list-folder-manifest.sh` exits 0 and emits valid JSON with `repo`, `folder`, `ts`, and `files[]` (empty array if folder missing).  
- `bin/dataset-enrich.sh` accepts `MANIFEST_FILE`, skips per-file listing when manifest is valid, and downloads via CDN URL first with authenticated `hf_hub_download` fallback on 404.  
- Output shards are written to deterministic path `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` and contain projected `{prompt, response}` pairs.  
- No 429/403 errors appear in logs during a smoke run with a single shard and a pre-generated manifest.

## review — qa @ 2026-05-03T01:16:54.098994Z

PASS: change approved and implementable

1. **Acceptance criteria**
- `bin/list-folder-manifest.sh` exits 0 and emits valid JSON containing required keys `repo`, `folder`, `ts` (ISO-8601 UTC), and `files` (array of objects with `path`, `sha`, `size`); emits `files: []` when folder missing.
- `bin/dataset-enrich.sh` with valid `MANIFEST_FILE` skips all `list_repo_tree` calls and processes only files listed in the manifest.
- `bin/dataset-enrich.sh` downloads each file via CDN URL first (`https://huggingface.co/datasets/{repo}/resolve/main/{path}`) and falls back to authenticated `hf_hub_download` only on CDN 404.
- Output shards are written to deterministic path `batches/public-merged/{date}/shard{N}-{HHMMSS}.jsonl` where `{date}` matches the folder date, `{N}` is zero-padded shard index, and `{HHMMSS}` is UTC time of creation.
- Each line in output shards is valid JSON containing projected `{prompt, response}` pairs derived from the ingested file.
- No 429 or 403 HTTP responses appear in logs during a smoke run with a pre-generated manifest and a single shard.

2. **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_list_folder_manifest.py
def test_emits_valid_json_with_required_keys(tmp_path, mocker):
    mock_api = mocker.patch("huggingface_hub.HfApi.list_repo_tree")
    mock_api.return_value = [
        {"path": "a.parquet", "lfs": {"sha256": "abc", "size": 1024}},
        {"path": "b.jsonl", "lfs": {"sha256": "def", "size": 2048}},
    ]
    out = tmp_path / "manifest.json"
    run_script("bin/list-folder-manifest.sh", ["repo", "folder", str(out)])
    data = json.loads(out.read_text())
    assert data["repo"] == "repo"
    assert data["folder"] == "folder"
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", data["ts"])
    assert len(data["files"]) == 2
    assert all(k in data["files"][0] for k in ("path", "sha", "size"))

def test_missing_folder_emits_empty_files(tmp_path, mocker):
    mock_api = mocker.patch("huggingface_hub.HfApi.list_repo_tree")
    mock_api.side_effect = RepositoryNotFoundError()
    out = tmp_path / "manifest.json"
    run_script("bin/list-folder-manifest.sh", ["repo", "folder", str(out)])
    data = json.loads(out.read_text())
    assert data["files"] == []
    assert data["repo"] == "repo"

# tests/unit/test_file_io.py
def test_download_via_cdn_uses_curl_then_fallback(mocker, tmp_path):
    curl = mocker.patch("subprocess.run")
    hf_download = mocker.patch("huggingface_hub.hf_hub_download")
    dest = tmp_path / "file"
    # CDN success
    curl.return_value.returncode = 0
    download_via_cdn("repo", "path/file", dest)
    assert "huggingface.co/datasets/repo/resolve/main/path/file" in curl.call_args[0][0]
    assert hf_download.call_count == 0
    # CDN 404 -> fallback
    curl.return_value.returncode = 22  # curl 22 = HTTP error
    hf_download.return_value = str(tmp_path / "hf_file")
    (tmp_path / "hf_file").write_text("x")
    download_via_cdn("repo", "path/file", dest)
    assert hf_download.call_count == 1

def test_project_to_pair_parquet(mocker, tmp_path):
    import pyarrow as pa
    table = pa.table({"prompt": ["hi"], "response": ["ok"]})
    path = tmp_path / "x.parquet"
    pq.write_table(table, path)
    pairs = list(project_to_pair(str(path)))
    assert pairs == [{"prompt": "hi", "response": "ok"}]

# tests/unit/test_dataset_enrich.py
def test_with_manifest_skips_listing(mocker, tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "repo": "repo", "folder": "folder", "ts": "...",
        "files": [{"path": "a.parquet", "sha": "x", "size": 10}]
    }))
    list_mock = mocker.patch("huggingface_hub.HfApi.list_repo_tree")
    download_mock = mocker.patch("lib.file_io.download_via_cdn")
    project_mock = mocker.patch("lib.file_io.project_to_pair", return_value=[{"prompt": "p", "response": "r"}])
    shard_mock = mocker.patch("lib.shard.upload_shard")
    run_dataset_enrich
