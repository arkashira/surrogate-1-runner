import json
import pyarrow.parquet as pq
import requests
import io
import os
import time
import logging
from typing import Iterator, Dict, Any

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = int(os.getenv("CDN_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("CDN_RETRIES", "3"))
BACKOFF_FACTOR = float(os.getenv("CDN_BACKOFF", "1.5"))

HF_TOKEN = os.getenv("HF_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}


def _fetch_cdn(url: str) -> bytes:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT, stream=True)
            resp.raise_for_status()
            return resp.content
        except Exception as exc:
            wait = BACKOFF_FACTOR ** attempt
            logger.warning("CDN fetch failed (attempt %s/%s) %s: %s", attempt, MAX_RETRIES, url, exc)
            if attempt == MAX_RETRIES:
                raise
            time.sleep(wait)
    raise RuntimeError(f"Failed to fetch {url}")


def read_jsonl(content: bytes) -> Iterator[Dict[str, Any]]:
    for line in io.BytesIO(content).read().splitlines():
        if not line:
            continue
        try:
            yield json.loads(line.decode("utf-8"))
        except Exception:
            continue


def read_parquet(content: bytes) -> Iterator[Dict[str, Any]]:
    try:
        table = pq.read_table(io.BytesIO(content))
        for batch in table.to_batches(max_chunksize=1000):
            cols = batch.column_names
            # Try common prompt/response names; fallback to first two text cols.
            prompt_col = next((c for c in ("prompt", "instruction", "input", "question") if c in cols), None)
            response_col = next((c for c in ("response", "output", "answer", "completion") if c in cols), None)

            if prompt_col and response_col:
                prompts = batch.column(cols.index(prompt_col)).to_pylist()
                responses = batch.column(cols.index(response_col)).to_pylist()
                for p, r in zip(prompts, responses):
                    if isinstance(p, str) and isinstance(r, str) and p.strip() and r.strip():
                        yield {"prompt": p.strip(), "response": r.strip()}
            else:
                # fallback: project first two string columns
                projected = []
                for col in cols:
                    if len(projected) >= 2:
                        break
                    col_vals = batch.column(cols.index(col)).to_pylist()
                    if col_vals and isinstance(col_vals[0], str):
                        projected.append(col_vals)
                if len(projected) == 2:
                    for a, b in zip(projected[0], projected[1]):
                        if isinstance(a, str) and isinstance(b, str) and a.strip() and b.strip():
                            yield {"prompt": a.strip(), "response": b.strip()}
    except Exception as exc:
        logger.warning("Parquet decode failed: %s", exc)


def stream_records_from_cdn(file_entry: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    url = file_entry["cdn_url"]
    content = _fetch_cdn(url)
    path = file_entry["path"]
    if path.endswith(".parquet"):
        yield from read_parquet(content)
    else:
        yield from read_jsonl(content)