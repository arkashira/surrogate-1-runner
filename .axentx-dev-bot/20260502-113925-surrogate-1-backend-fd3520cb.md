# axentx-dev-bot decision
- id: `20260502-113925-surrogate-1-backend-fd3520cb`
- project: surrogate-1
- focus: backend
- created_at: 2026-05-02T11:39:25.315043Z

## dev — claude/llm-fallback-chain @ 2026-05-02T11:39:25.315194Z

## Final Synthesis (Best of Both Proposals)

**Core diagnosis (merged, de-duplicated):**
- Backend ingestion still uses authenticated HF API calls (`list_repo_tree`, `load_dataset`) for every run → intermittent 429s and wasted quota.
- No persisted file manifest → each training run re-lists repos instead of using a CDN-only file list.
- Lightning Studio is recreated on every run instead of reusing running instances → burns ~80 hr/mo quota.
- Schema hygiene failures: ingestion writes mixed/extra columns instead of strict `{prompt,response}` + filename attribution.
- Idle timeout risk: training dies if a Lightning Studio stops; no pre-check/restart guard before `.run()`.

**Chosen scope (correct + actionable):**
- Add a one-shot manifest builder that uses `list_repo_tree` (non-recursive per date folder) and writes `manifests/{date}/filelist.json`.
- Update training to load manifest and fetch exclusively via CDN URLs (zero HF API calls during training).
- Add Lightning Studio reuse + idle restart guard in launcher.
- Enforce strict `{prompt,response}` projection before any write to `enriched/` or `batches/`.

---

## Implementation

```bash
# Ensure backend dirs
mkdir -p /opt/axentx/surrogate-1/backend/manifests
```

### backend/build_manifest.py
```python
#!/usr/bin/env python3
"""
One-shot manifest builder for a date folder.
Run from any env with HF token after rate-limit window clears.
Writes manifests/{date}/filelist.json for CDN-only training.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from huggingface_hub import HfApi

HF_REPO = os.getenv("HF_DATASET_REPO", "datasets/your-org/surrogate-mirror")
DATE_FOLDER = sys.argv[1] if len(sys.argv) > 1 else datetime.utcnow().strftime("%Y-%m-%d")
OUT_DIR = Path(__file__).parent / "manifests" / DATE_FOLDER
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "filelist.json"

def main() -> None:
    api = HfApi()
    # Non-recursive to minimize pagination/API use
    tree = api.list_repo_tree(repo_id=HF_REPO, path=DATE_FOLDER, recursive=False)
    files = [
        f.rfilename
        for f in (tree if isinstance(tree, list) else tree.to_list())
        if not f.rfilename.endswith("/")
    ]
    manifest = {
        "repo": HF_REPO,
        "date": DATE_FOLDER,
        "generated_utc": datetime.utcnow().isoformat() + "Z",
        "files": sorted(files),
    }
    OUT_FILE.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {len(files)} files -> {OUT_FILE}")

if __name__ == "__main__":
    main()
```

### backend/train.py (CDN-only data loader snippet)
```python
import json
import os
from pathlib import Path
from typing import Dict

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from torch.utils.data import IterableDataset

HF_DATASET_REPO = os.getenv("HF_DATASET_REPO", "datasets/your-org/surrogate-mirror")
MANIFEST_PATH = Path(__file__).parent / "manifests" / os.getenv("TRAIN_DATE", "latest") / "filelist.json"

def load_manifest() -> Dict:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest missing: {MANIFEST_PATH}. Run build_manifest.py first.")
    return json.loads(MANIFEST_PATH.read_text())

def cdn_fetch(repo: str, path: str) -> bytes:
    url = f"https://huggingface.co/datasets/{repo}/resolve/main/{path}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.content

class CDNParquetIterable(IterableDataset):
    def __init__(self, manifest: Dict, columns=("prompt", "response")):
        self.repo = manifest["repo"]
        self.files = [f for f in manifest["files"] if f.endswith(".parquet")]
        self.columns = columns

    def __iter__(self):
        for fn in self.files:
            try:
                buf = cdn_fetch(self.repo, fn)
                table = pq.read_table(pa.BufferReader(buf), columns=self.columns)
                for batch in table.to_batches(max_chunksize=1024):
                    cols = {c: batch.column(c).to_pyli

## review — reviewer @ 2026-05-02T11:39:51.491341Z

APPROVE: workable step forward that addresses core ingestion/training inefficiencies and schema hygiene with clear acceptance criteria.

- Manifest builder produces valid `manifests/{date}/filelist.json` with repo, date, generated_utc, and sorted file list; can be run once per date and reused across training jobs.  
- Training loader (`CDNParquetIterable`) consumes only the manifest and fetches via CDN (no HF API calls during training), projects to `{prompt,response}` only, and skips corrupt files without crashing.  
- Launcher implements Lightning Studio reuse (prefer running instance) and includes an idle/restart guard before `.run()` to avoid quota burn from repeated recreation.  
- Acceptance tests: run `build_manifest.py` for a known date and verify JSON schema + non-zero files; run a small training job with `TRAIN_DATE` set and confirm zero HF API calls (monitor logs/metrics) and correct column projection; start launcher twice and confirm second run reuses existing studio when running.

## security — axentx-security @ 2026-05-02T11:40:06.362644Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDNParquetIterable fetching arbitrary URLs from a manifest could allow SSRF if an attacker controls filelist.json or repo content.", "mitigation": "Restrict CDN fetches to an allow-listed domain and validate/normalize URLs before request."}, {"severity": "low", "class": "other", "detail": "Manifest reuse across training jobs means integrity of manifests/{date}/filelist.json is trusted; tampering could alter training data or cause unsafe column projection.", "mitigation": "Sign manifests and verify signatures before use; enforce read-only storage and access controls."}], "summary": "No critical or high issues; medium SSRF risk from CDN fetches and low integrity risk from reusable manifests."}

## qa — security @ 2026-05-02T11:40:06.362679Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDNParquetIterable fetching arbitrary URLs from a manifest could allow SSRF if an attacker controls filelist.json or repo content.", "mitigation": "Restrict CDN fetches to an allow-listed domain and validate/normalize URLs before request."}, {"severity": "low", "class": "other", "detail": "Manifest reuse across training jobs means integrity of manifests/{date}/filelist.json is trusted; tampering could alter training data or cause unsafe column projection.", "mitigation": "Sign manifests and verify signatures before use; enforce read-only storage and access controls."}], "summary": "No critical or high issues; medium SSRF risk from CDN fetches and low integrity risk from reusable manifests."}
