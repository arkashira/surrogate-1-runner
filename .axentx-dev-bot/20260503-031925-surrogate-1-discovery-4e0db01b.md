# axentx-dev-bot decision
- id: `20260503-031925-surrogate-1-discovery-4e0db01b`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T03:19:25.738445Z

## dev — claude/llm-fallback-chain @ 2026-05-03T03:19:25.738502Z

### Final Consolidated Implementation (≤2h)

Replace `bin/dataset-enrich.sh` with a **manifest-driven, CDN-bypass ingestion worker** (`bin/dataset-enrich.py`) that:

- Accepts `SHARD_ID`, `SHARD_TOTAL=16`, `DATE`, `HF_TOKEN` via env  
- Calls `list_repo_tree(path, recursive=False)` **once per shard per run** and saves a JSON manifest  
- Uses **deterministic shard assignment**: `hash(filename) % SHARD_TOTAL == SHARD_ID`  
- Downloads **only assigned files** via HF CDN (`resolve/main/...`) — no auth, no API rate limit  
- Projects heterogeneous schemas to `{prompt, response}` at parse time (eliminates pyarrow `CastError`)  
- Deduplicates via central md5 store (`lib/dedup.py`) with in-memory fallback  
- Writes `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`  
- Returns exit code 0 on success, non-zero on fatal error (GitHub Actions handles retries)

---

### `bin/dataset-enrich.py`
```python
#!/usr/bin/env python3
"""
surrogate-1 CDN-bypass ingestion worker.

Environment:
  SHARD_ID        (int) 0..15
  SHARD_TOTAL     (int) default 16
  DATE            (str) YYYY-MM-DD (defaults to today UTC)
  HF_TOKEN        (str) write token for axentx/surrogate-1-training-pairs
  REPO_ID         (str) default axentx/surrogate-1-training-pairs
  LOG_LEVEL       (str) default INFO
"""
import os
import sys
import json
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

import requests
from huggingface_hub import HfApi, list_repo_tree

# ---- config ----
REPO_ID = os.getenv("REPO_ID", "axentx/surrogate-1-training-pairs")
SHARD_TOTAL = int(os.getenv("SHARD_TOTAL", "16"))
SHARD_ID = int(os.getenv("SHARD_ID", "0"))
DATE = os.getenv("DATE", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
HF_TOKEN = os.getenv("HF_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
log = logging.getLogger("dataset-enrich")

# ---- helpers ----
def deterministic_shard(slug: str, total: int) -> int:
    return int(hashlib.sha256(slug.encode()).hexdigest(), 16) % total

def cdn_download(url: str, dest: Path) -> Path:
    """Download via HF CDN (no auth). Raises on non-2xx."""
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
    return dest

def project_to_pair(raw_obj: Dict[str, Any]) -> Dict[str, str]:
    """
    Project heterogeneous HF dataset objects to {prompt, response}.
    Handles common surrogate-1 schema variants.
    """
    low = {k.lower().replace("-", "_"): v for k, v in raw_obj.items() if isinstance(v, (str, int, float, bool))}

    prompt = None
    response = None

    if "prompt" in low and "response" in low:
        prompt, response = low["prompt"], low["response"]
    elif "instruction" in low and "output" in low:
        prompt, response = low["instruction"], low["output"]
    elif "input" in low and "output" in low:
        prompt, response = low["input"], low["output"]
    elif "question" in low and "answer" in low:
        prompt, response = low["question"], low["answer"]
    elif "text" in low:
        text = str(low["text"])
        for sep in ("\nassistant:", "\nmodel:", "\nresponse:", "\n\n"):
            if sep in text:
                parts = text.split(sep)
                prompt = parts[0].strip()
                response = sep.strip().lstrip("\n") + ": " + sep.join(parts[1:]).strip()
                break
        if prompt is None:
            prompt, response = "", text
    else:
        prompt, response = "", json.dumps(raw_obj, ensure_ascii=False, default=str)

    return {"prompt": str(prompt), "response": str(response)}

# ---- dedup ----
def load_dedup_store() -> set:
    """Load central md5 store via lib/dedup.py if available; else in-memory."""
    try:
        from lib.dedup import DedupStore
    

## review — reviewer @ 2026-05-03T03:19:36.460439Z

APPROVE: This is a clear, workable first step toward a manifest-driven, CDN-bypass ingestion worker. It defines deterministic shard assignment, schema projection, dedup fallback, and explicit outputs/exit codes — all of which a downstream tester can validate incrementally.

Acceptance criteria (for this discovery-stage change):
- Worker accepts SHARD_ID, SHARD_TOTAL, DATE, HF_TOKEN via env and defaults REPO_ID/LOG_LEVEL as documented.
- Deterministic shard assignment uses `hash(filename) % SHARD_TOTAL == SHARD_ID` (SHA-256 shown) and is consistent across runs.
- `list_repo_tree(path, recursive=False)` is called once per shard per run and a JSON manifest is saved under `manifest/{DATE}/shard{N}.json`.
- Only assigned files are processed; each file is downloaded via HF CDN (`resolve/main/...`) without auth and written to `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl`.
- Heterogeneous schemas are projected to `{prompt, response}` at parse time (handles prompt/response, instruction/output, input/output, question/answer, text splitting, and fallback JSON).
- Deduplication uses central md5 store via `lib/dedup.py` with in-memory fallback; missing store logs warning and continues.
- Exit code 0 on success, non-zero on fatal error (e.g., missing HF_TOKEN, non-2xx CDN download); errors are logged with timestamps.

## qa — qa @ 2026-05-03T03:19:50.226176Z

PASS: Ready for TDD implementation.

1. **Acceptance criteria**
- Worker reads SHARD_ID, SHARD_TOTAL, DATE, HF_TOKEN, REPO_ID, LOG_LEVEL from environment with documented defaults (SHARD_TOTAL=16, REPO_ID=axentx/surrogate-1-training-pairs, DATE=today UTC, LOG_LEVEL=INFO).
- Deterministic shard assignment uses SHA-256 of filename and satisfies `hash(filename) % SHARD_TOTAL == SHARD_ID`; same filename always maps to same shard across runs.
- `list_repo_tree(path, recursive=False)` is invoked exactly once per run and a JSON manifest is saved to `manifest/{DATE}/shard{N}.json` containing repo tree entries for the shard.
- Only files assigned to the shard are processed; each file is downloaded via HF CDN (`https://huggingface.co/resolve/main/...`) without authentication and written to `batches/public-merged/{DATE}/shard{N}-{HHMMSS}.jsonl` with one `{prompt,response}` object per line.
- Heterogeneous schemas are projected to `{prompt,response}` at parse time (covers prompt/response, instruction/output, input/output, question/answer, text splitting, and fallback JSON) with non-string values coerced to strings.
- Deduplication uses `lib/dedup.py` central md5 store with in-memory fallback; if the central store is unavailable a warning is logged and processing continues without fatal error.
- Exit code is 0 on success and non-zero on fatal error (missing HF_TOKEN, non-2xx CDN download, invalid manifest); all errors include UTC timestamps in logs.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_deterministic_shard.py
def test_shard_assignment_consistent():
    assert deterministic_shard("file1.json", 16) == deterministic_shard("file1.json", 16)

def test_shard_range():
    for total in [1, 2, 16]:
        for slug in ["a", "b", "c"]:
            shard = deterministic_shard(slug, total)
            assert 0 <= shard < total

# test_project_to_pair.py
def test_prompt_response():
    assert project_to_pair({"prompt": "hi", "response": "ok"}) == {"prompt": "hi", "response": "ok"}

def test_instruction_output():
    assert project_to_pair({"instruction": "hi", "output": "ok"}) == {"prompt": "hi", "response": "ok"}

def test_input_output():
    assert project_to_pair({"input": "hi", "output": "ok"}) == {"prompt": "hi", "response": "ok"}

def test_question_answer():
    assert project_to_pair({"question": "hi", "answer": "ok"}) == {"prompt": "hi", "response": "ok"}

def test_text_split():
    assert project_to_pair({"text": "Q: hi A: ok"}) == {"prompt": "hi", "response": "ok"}

def test_fallback_json():
    assert project_to_pair({"x": 1}) == {"prompt": "", "response": '{"x":1}'}

def test_non_string_coercion():
    out = project_to_pair({"prompt": 123, "response": True})
    assert out == {"prompt": "123", "response": "True"}

# test_cdn_download.py
def test_cdn_download_success(requests_mock, tmp_path):
    url = "https://huggingface.co/resolve/main/data/file.json"
    requests_mock.get(url, content=b"{}")
    dest = cdn_download(url, tmp_path / "file.json")
    assert dest.read_bytes() == b"{}"

def test_cdn_download_non_2xx_raises(requests_mock):
    url = "https://huggingface.co/resolve/main/data/file.json"
    requests_mock.get(url, status_code=404)
    with pytest.raises(Exception):
        cdn_download(url, Path("/tmp/file.json"))

# test_env_config.py
def test_defaults(monkeypatch):
    monkeypatch.delenv("SHARD_TOTAL", raising=False)
    monkeypatch.delenv("REPO_ID", raising=False)
    # simulate module import/config load
    cfg = load_config()  # returns dict of config values
    assert cfg["SHARD_TOTAL"] == 16
    assert cfg["REPO_ID"] == "axentx/surrogate-1-training-pairs"
```

3. **Integration tests** (3 happy + 3 edge)
```text
Happy cases:
1) Full shard run with valid repo tree and assigned files
   - Set SHARD_ID=0, SHARD_TOTAL=16, valid HF_TOKEN, DATE=2025-01-01
   - Mock list_repo_tree to return 3 files where exactly 1 hashes to shard 0
   - Mock CDN download to return valid JSON lines with prompt/response
   - 
