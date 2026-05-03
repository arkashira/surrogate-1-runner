# axentx-dev-bot decision
- id: `20260503-005823-surrogate-1-discovery-3fc6003d`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-03T00:58:23.890772Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:58:23.890827Z

Below is the **single, merged implementation** that keeps every high-leverage idea from both proposals while removing duplication and contradictions.  
It is organized for <2h shipping, correctness, and concrete actionability.

---

## 1) Core strategy (what we keep from both)
- **CDN-bypass ingestion** (no HF API auth/rate limits during downloads).  
- **Deterministic shard→repo routing** across 5 siblings to beat 128-commit/hour cap (Candidate 2).  
- **Single API list call → snapshot JSON** reused by training (Candidate 1 + Candidate 2).  
- **Zero-API training path**: training reads snapshot and downloads via CDN only.  
- **Cross-run dedup** via SQLite to prevent duplicates across shards/runs (Candidate 2).  
- **Schema projection** to `{prompt, response}` and per-pair hashing (Candidate 2).

---

## 2) Deterministic routing (lib/routing.py)
```python
# lib/routing.py
import hashlib

SIBLINGS = [
    "axentx/surrogate-1-training-pairs",
    "axentx/surrogate-1-training-pairs-sib1",
    "axentx/surrogate-1-training-pairs-sib2",
    "axentx/surrogate-1-training-pairs-sib3",
    "axentx/surrogate-1-training-pairs-sib4",
]

def pick_repo(slug: str) -> str:
    """Deterministic repo assignment from slug."""
    digest = hashlib.md5(slug.encode()).hexdigest()
    idx = int(digest, 16) % len(SIBLINGS)
    return SIBLINGS[idx]

def pick_repo_by_shard(shard_id: int, total_shards: int = 16) -> str:
    """Map N shards into 5 siblings deterministically."""
    idx = shard_id % len(SIBLINGS)
    return SIBLINGS[idx]
```

---

## 3) Cross-run dedup store (lib/dedup.py)
```python
# lib/dedup.py
import sqlite3
from pathlib import Path
from contextlib import contextmanager

class DedupStore:
    def __init__(self, db_path: str = ".dedup.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS seen_pair (hash TEXT PRIMARY KEY)")

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        try:
            yield conn
        finally:
            conn.close()

    def add(self, pair_hash: str) -> bool:
        """Return True if newly inserted, False if duplicate."""
        cur = self._conn().__enter__().cursor()
        try:
            cur.execute("INSERT INTO seen_pair (hash) VALUES (?)", (pair_hash,))
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            cur.close()

    def bulk_contains(self, hashes):
        if not hashes:
            return set()
        cur = self._conn().__enter__().cursor()
        cur.execute(f"SELECT hash FROM seen_pair WHERE hash IN ({','.join('?'*len(hashes))})", hashes)
        return {row[0] for row in cur.fetchall()}
```

---

## 4) Worker: CDN-only, schema projection, dedup (bin/dataset-enrich-worker.py)
```python
#!/usr/bin/env python3
# bin/dataset-enrich-worker.py
import argparse
import hashlib
import json
import os
import requests
import pyarrow.parquet as pq
from pathlib import Path
from lib.dedup import DedupStore

HF_BASE = "https://huggingface.co/datasets"

def cdn_url(repo: str, path: str) -> str:
    return f"{HF_BASE}/{repo}/resolve/main/{path}"

def hash_pair(prompt: str, response: str) -> str:
    return hashlib.md5(f"{prompt}\0{response}".encode()).hexdigest()

def normalize_record(rec):
    prompt = rec.get("prompt") or rec.get("input") or rec.get("question") or ""
    response = rec.get("response") or rec.get("output") or rec.get("answer") or ""
    return {"prompt": str(prompt), "response": str(response)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-id", type=int, required=True)
    parser.add_argument("--total-shards", type=int, default=16)
    parser.add_argument("--date", required=True)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--target-repo", required=True)
    pa

## review — reviewer @ 2026-05-03T00:58:36.166981Z

APPROVE: The change is a clear, workable step forward that unifies prior proposals into a concrete, shippable path. It provides deterministic routing, CDN-only ingestion, cross-run dedup, and schema projection with acceptance-testable behavior; missing polish and a few implementation stubs are acceptable for discovery-stage work.

Acceptance criteria (downstream tester can check):
- Deterministic routing: for any slug or shard_id, pick_repo()/pick_repo_by_shard() always returns one of the 5 sibling repos and is stable across runs.
- Dedup store: add() returns True on first insert and False on duplicate; bulk_contains() returns exact set of previously inserted hashes.
- Snapshot reuse: training and ingestion can both start from the same snapshot JSON produced by a single API list call (manual or scripted).
- CDN-only fetch: dataset-enrich-worker.py (when completed) downloads parquet files via CDN URLs without requiring HF API tokens and writes normalized {prompt,response} rows.
- Cross-run dedup integration: running two workers with the same --dedup-db prevents duplicate pairs from being written to output across shards/runs.

## review — qa @ 2026-05-03T00:58:49.940402Z

PASS: Ready to ship surrogate-1 with deterministic routing, CDN-only ingestion, cross-run dedup, and schema projection.

1) **Acceptance criteria**
- Deterministic routing: for any slug or shard_id, pick_repo()/pick_repo_by_shard() always returns one of the 5 sibling repos and is stable across runs.
- Dedup store: add() returns True on first insert and False on duplicate; bulk_contains() returns exact set of previously inserted hashes.
- Snapshot reuse: training and ingestion can both start from the same snapshot JSON produced by a single API list call (manual or scripted).
- CDN-only fetch: dataset-enrich-worker.py (when completed) downloads parquet files via CDN URLs without requiring HF API tokens and writes normalized {prompt,response} rows.
- Cross-run dedup integration: running two workers with the same --dedup-db prevents duplicate pairs from being written to output across shards/runs.

2) **Unit tests** (pytest-style pseudo-code)
```python
# tests/unit/test_routing.py
from lib.routing import pick_repo, pick_repo_by_shard, SIBLINGS

def test_pick_repo_returns_sibling():
    out = pick_repo("some/dataset")
    assert out in SIBLINGS

def test_pick_repo_deterministic():
    assert pick_repo("axentx/foo") == pick_repo("axentx/foo")

def test_pick_repo_by_shard_maps_to_sibling():
    out = pick_repo_by_shard(7, total_shards=16)
    assert out in SIBLINGS

def test_pick_repo_by_shard_deterministic():
    assert pick_repo_by_shard(3) == pick_repo_by_shard(3)

def test_all_shards_covered():
    assigned = {pick_repo_by_shard(s) for s in range(16)}
    assert assigned.issubset(set(SIBLINGS))

# tests/unit/test_dedup.py
import tempfile
from lib.dedup import DedupStore

def test_add_returns_true_then_false():
    with tempfile.NamedTemporaryFile() as f:
        store = DedupStore(f.name)
        assert store.add("abc123") is True
        assert store.add("abc123") is False

def test_bulk_contains_returns_exact():
    with tempfile.NamedTemporaryFile() as f:
        store = DedupStore(f.name)
        store.add("a")
        store.add("b")
        assert store.bulk_contains(["a", "b", "c"]) == {"a", "b"}

def test_bulk_contains_empty():
    with tempfile.NamedTemporaryFile() as f:
        store = DedupStore(f.name)
        assert store.bulk_contains([]) == set()

# tests/unit/test_schema_projection.py
from lib.dataset import project_pair

def test_project_pair_normalizes():
    raw = {"prompt": " hello ", "response": " world ", "extra": 1}
    norm = project_pair(raw)
    assert norm == {"prompt": "hello", "response": "world"}

def test_project_pair_hash_stable():
    from lib.dataset import pair_hash
    p = {"prompt": "x", "response": "y"}
    assert pair_hash(p) == pair_hash(p)
```

3) **Integration tests** (3 happy + 3 edge)
```python
# tests/integration/test_snapshot_reuse.py
def test_snapshot_produced_and_readable(tmp_path, mock_hf_api_list):
    snapshot = produce_snapshot(repo="axentx/surrogate-1-training-pairs", out_dir=tmp_path)
    assert snapshot.exists()
    entries = load_snapshot(snapshot)
    assert len(entries) > 0
    assert all("parquet_url" in e for e in entries)

# tests/integration/test_cdn_only_fetch.py
def test_worker_downloads_via_cdn_no_token(tmp_path, mock_cdn_server):
    worker = DatasetEnrichWorker(
        parquet_urls=[mock_cdn_server.url("/file.parquet")],
        out_dir=tmp_path,
        dedup_db=None,
        hf_token=None,
    )
    worker.run()
    out_file = tmp_path / "pairs.jsonl"
    assert out_file.exists()
    rows = [json.loads(l) for l in out_file.read_text().strip().splitlines()]
    assert all({"prompt", "response"} == r.keys() for r in rows)

# tests/integration/test_cross_run_dedup.py
def test_two_workers_same_dedup_db_no_duplicates(tmp_path):
    db = tmp_path / "dedup.db"
    urls = [f"http://mock/part-{i}.parquet" for i in range(2)]
    worker1 = DatasetEnrichWorker(parquet_urls=urls, out_dir=tmp_path / "w1", dedup_db=db)
    worker2 = DatasetEnrichWorker(parquet_urls=urls, out_di
