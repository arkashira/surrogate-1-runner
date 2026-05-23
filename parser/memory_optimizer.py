"""
Memory Optimizer for large data‑stream parsing.

Provides:
* `StreamingJSONParser` – incremental JSON parsing using ijson when available,
  falling back to line‑by‑line parsing. Yields one Python object per JSON value
  without loading the entire file into memory.
* `ByteArrayPool` – a simple reusable pool of pre‑allocated ``bytearray`` objects
  to avoid repeated allocations during chunked reads.
* `optimize_memory` – decorator that clears ``functools.lru_cache`` caches and
  forces garbage collection after the wrapped function returns, helping to keep
  the process’s resident set size low for long‑running workers.

Typical usage: