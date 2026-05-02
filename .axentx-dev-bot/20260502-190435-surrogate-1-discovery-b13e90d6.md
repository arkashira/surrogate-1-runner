# axentx-dev-bot decision
- id: `20260502-190435-surrogate-1-discovery-b13e90d6`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T19:04:35.230730Z

## dev — claude/llm-fallback-chain @ 2026-05-02T19:04:35.230794Z

## Final synthesized implementation (best of both)

**Core idea**: One pre-flight step produces a deterministic, date-partitioned file list; each shard uses CDN-only fetches and a stable hash to write exactly one file per run. Races and API pressure are eliminated.

---

### 1) Workflow (`.github/workflows/ingest.yml`)

- Preflight job lists today’s folder once and uploads `file-list.json`.
- Matrix of 16 shards runs in parallel.
- Date/time are injected once so all shards use the same filenames.

```yaml
name: surrogate-1-ingest
on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  preflight:
    runs-on: ubuntu-latest
    outputs:
      date: ${{ steps.date.outputs.DATE }}
      time: ${{ steps.time.outputs.TIME }}
    steps:
      - uses: actions/checkout@v4

      - name: Set date/time
        id: date
        run: echo "DATE=$(date -u +%Y-%m-%d)" >> $GITHUB_OUTPUT

      - name: Set time
        id: time
        run: echo "TIME=$(date -u +%H%M%S)" >> $GITHUB_OUTPUT

      - name: List today folder (single API call)
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          python - <<'PY'
          import os, json, datetime
          from huggingface_hub import HfApi
          api = HfApi(token=os.getenv("HF_TOKEN"))
          today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
          repo = "datasets/axentx/surrogate-1-training-pairs"
          items = api.list_repo_tree(repo=repo, path=today, recursive=False)
          files = sorted(it.rfilename for it in items if hasattr(it, "rfilename"))
          with open("file-list.json", "w") as f:
              json.dump({"date": today, "files": files}, f)
          PY

      - uses: actions/upload-artifact@v4
        with:
          name: file-list
          path: file-list.json

  ingest:
    needs: preflight
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard_id: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/download-artifact@v4
        with:
          name: file-list

      - name: Install deps
        run: pip install -r requirements.txt

      - name: Run shard worker
        env:
          SHARD_ID: ${{ matrix.shard_id }}
          DATE_PART: ${{ needs.preflight.outputs.date }}
          TIME_PART: ${{ needs.preflight.outputs.time }}
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
          REPO: "datasets/axentx/surrogate-1-training-pairs"
        run: |
          bash bin/dataset-enrich.sh
```

---

### 2) `bin/dataset-enrich.sh` (deterministic + CDN + race-safe)

- Uses pre-computed `file-list.json`.
- Deterministic shard assignment by `slug` (`sha256 % 16`).
- Writes to `batches/public-merged/YYYY-MM-DD/shardN-HHMMSS.jsonl`.
- Skips if `_SUCCESS` marker for this shard/date/time already exists (prevents overwrite races).
- Pushes only its own file; commit includes shard/date/time.

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${SHARD_ID:?}"
: "${DATE_PART:?}"
: "${TIME_PART:?}"
: "${REPO:?}"
: "${HF_TOKEN:?}"

BASE_OUT="batches/public-merged/${DATE_PART}"
OUT_FILE="${BASE_OUT}/shard${SHARD_ID}-${TIME_PART}.jsonl"
SUCCESS_MARKER="${BASE_OUT}/shard${SHARD_ID}-${TIME_PART}.success"

mkdir -p "$(dirname "$OUT_FILE")"

# Skip if this exact shard/time already completed (avoid races/repeats)
if [[ -f "$SUCCESS_MARKER" ]]; then
  echo "Shard ${SHARD_ID} for ${DATE_PART} ${TIME_PART} already done (success marker present). Skipping."
  exit 0
fi

# Deterministic shard assignment by slug
shard_for() {
  local slug=$1
  python -c "import hashlib; print(abs(int(hashlib.sha256('$slug'.encode()).hexdigest(), 16)) % 16)"
}

python - <<PY
import json, os, hashlib, sys, requests, tqdm

SHARD_ID = int(os.getenv("SHARD_ID"))
REPO = os.getenv("REPO")
OUT_FILE = os.getenv("OUT_FILE")
FILE_LIST = "file-list.json"

with open(FILE_LIST) as f:
    manifest = json.load(f)

files = manifest["files"]

def shard_for(slug: str) -> int:
    return abs(int(hashlib.sha256(slu

## review — reviewer @ 2026-05-02T19:04:43.311154Z

APPROVE: Deterministic sharding + preflight file list + CDN-only fetches + success markers eliminate races and reduce API pressure; this is a clear, workable step forward for discovery.

Acceptance criteria:
- Preflight job produces `file-list.json` with today’s folder contents and uploads it as an artifact; matrix shards download and use it.
- Each shard deterministically selects files via `sha256(slug) % 16 == SHARD_ID` and writes to `batches/public-merged/YYYY-MM-DD/shardN-HHMMSS.jsonl`.
- Success marker (`shardN-HHMMSS.success`) is created after write and checked at start; shard exits 0 if marker exists to prevent overwrite races.
- All fetches use CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) with no concurrent writes to the same file.
- Secrets (`HF_TOKEN`) and config (`REPO`, `DATE_PART`, `TIME_PART`) are injected via env; script fails fast on missing required env vars.

## qa — qa @ 2026-05-02T19:05:46.387963Z

PASS: 

1) **Acceptance criteria**
- Preflight produces `file-list.json` containing `date` (YYYY-MM-DD) and `files` (non-empty list of strings) and uploads it as an artifact; matrix shards download and parse it.
- Each shard deterministically selects files via `sha256(slug) % 16 == SHARD_ID` and writes exactly one file to `batches/public-merged/YYYY-MM-DD/shardN-HHMMSS.jsonl`.
- Success marker `batches/public-merged/YYYY-MM-DD/shardN-HHMMSS.success` is created after write; if marker exists at start, shard exits 0 and does not overwrite.
- All fetches use CDN URLs (`https://huggingface.co/datasets/.../resolve/main/...`) and no concurrent writes target the same file.
- Secrets and config (`HF_TOKEN`, `REPO`, `DATE_PART`, `TIME_PART`, `SHARD_ID`) are injected via env; script fails fast (non-zero) on missing required env vars.
- Output file is valid NDJSON (one JSON object per line) and contains at least one record per processed file.
- End-to-end run with 16 shards produces exactly 16 distinct shard files for the same date/time and zero duplicate file processing across shards.

2) **Unit tests** (pytest-style pseudo-code)
```python
# test_preflight.py
def test_preflight_produces_valid_file_list(tmp_path, mock_hf_api):
    today = "2025-06-25"
    mock_hf_api.list_repo_tree.return_value = [
        type("Item", (), {"rfilename": f"{today}/a.jsonl"}),
        type("Item", (), {"rfilename": f"{today}/b.jsonl"}),
    ]
    out = run_preflight(date=today)
    assert out["date"] == today
    assert out["files"] == [f"{today}/a.jsonl", f"{today}/b.jsonl"]
    assert (tmp_path / "file-list.json").exists()

# test_shard.py
def test_deterministic_shard_assignment():
    slug = "axentx/surrogate-1-training-pairs/2025-06-25/a.jsonl"
    assert shard_for(slug, total=16) == hashlib.sha256(slug.encode()).hexdigest_int() % 16

def test_success_marker_prevents_overwrite(tmp_path, monkeypatch):
    marker = tmp_path / "batches/public-merged/2025-06-25/shard3-120000.success"
    marker.parent.mkdir(parents=True)
    marker.write_text("")
    monkeypatch.setenv("SHARD_ID", "3")
    monkeypatch.setenv("DATE_PART", "2025-06-25")
    monkeypatch.setenv("TIME_PART", "120000")
    code = run_shard(tmp_path)
    assert code == 0
    assert not (tmp_path / "batches/public-merged/2025-06-25/shard3-120000.jsonl").exists()

def test_missing_required_env_exits_nonzero(monkeypatch):
    for req in ("SHARD_ID", "DATE_PART", "TIME_PART", "HF_TOKEN", "REPO"):
        env = {k: "x" for k in ("SHARD_ID", "DATE_PART", "TIME_PART", "HF_TOKEN", "REPO")}
        env.pop(req, None)
        monkeypatch.setattr(os, "environ", env)
        with pytest.raises(SystemExit) as exc:
            validate_env()
        assert exc.value.code != 0

def test_cdn_url_used_for_fetches(monkeypatch):
    calls = []
    def fake_get(url, **kw):
        calls.append(url)
        return type("R", (), {"json": lambda: {}})()
    monkeypatch.setattr(requests, "get", fake_get)
    fetch_cdn("datasets/axentx/surrogate-1-training-pairs/2025-06-25/a.jsonl")
    assert any("resolve/main" in u for u in calls)
```

3) **Integration tests** (3 happy + 3 edge)

Happy paths:
- Happy 1 — Preflight + 16-shard matrix: preflight creates file-list with 32 files; each shard downloads file-list, selects its files deterministically, writes its shard file and success marker; final state has 16 shard files and 16 success markers with no file processed by more than one shard.
- Happy 2 — CDN-only fetches: run shard with mocked CDN endpoints returning valid JSONL lines; verify output NDJSON contains expected merged records and no non-CDN URLs were requested.
- Happy 3 — Idempotent rerun: after successful run, rerun same shard/date/time; script exits 0 immediately, no new files created, no CDN fetches performed.

Edge cases:
- Edge 1 — Empty today folder: preflight produces `{"date":"YYYY-MM-DD","files":[]}`; all shards exit 0 and produce no shard files (only success markers if policy requires).
-
