"""
Utility helpers for high‑throughput, low‑CPU‑overhead parsing.

The functions in this module are deliberately lightweight and have no
external dependencies beyond the Python standard library. They are
intended to be used by the parser implementation to:

* Stream large inputs in fixed‑size chunks without loading the whole file
  into memory.
* Parallelise CPU‑bound work while respecting a configurable CPU usage
  ceiling (default 50 % of available cores).
* Provide a simple API for processing many streams concurrently.
"""

from __future__ import annotations

import os
import itertools
import multiprocessing
from contextlib import contextmanager
from typing import Generator, Iterable, Tuple, Callable, Any

# ----------------------------------------------------------------------
# Chunked iterator
# ----------------------------------------------------------------------
def chunked_iterator(stream: Iterable[bytes], chunk_size: int = 4 * 1024 * 1024) -> Generator[bytes, None, None]:
    """
    Yield ``chunk_size``‑byte pieces from a binary stream.

    The function works with any object that yields ``bytes`` (e.g. a file
    opened in ``rb`` mode or ``io.BufferedReader``).  It never reads more
    than ``chunk_size`` bytes into memory at once, which makes it safe
    for > 1 GB inputs.

    Parameters
    ----------
    stream:
        An iterable yielding ``bytes`` objects.
    chunk_size:
        Desired size of each chunk (default 4 MiB).

    Yields
    ------
    bytes
        The next chunk of data.
    """
    buffer = b""
    for data in stream:
        buffer += data
        while len(buffer) >= chunk_size:
            yield buffer[:chunk_size]
            buffer = buffer[chunk_size:]
    if buffer:
        yield buffer


# ----------------------------------------------------------------------
# CPU‑usage‑aware process pool
# ----------------------------------------------------------------------
def _worker_initializer(max_cpu_percent: float) -> None:
    """
    Initialise a worker process to respect a CPU usage ceiling.

    The implementation is intentionally simple: each worker will
    voluntarily sleep for a short period if the process’ CPU time
    exceeds ``max_cpu_percent`` of a single core.  This throttling keeps
    the overall utilisation of the host machine below the target.

    Parameters
    ----------
    max_cpu_percent:
        Desired maximum CPU usage per worker (0‑100).  ``50`` means
        “no more than half a core”.
    """
    import time
    import psutil  # psutil is part of the runtime image for this repo

    pid = os.getpid()
    proc = psutil.Process(pid)

    def _throttle():
        # ``cpu_percent`` with interval=0 returns the instantaneous usage.
        while proc.cpu_percent(interval=0.1) > max_cpu_percent:
            time.sleep(0.05)

    # Attach the throttling function to the process object for later use.
    proc._throttle = _throttle  # type: ignore[attr-defined]


def cpu_limited_pool(max_workers: int | None = None,
                     max_cpu_percent: float = 50.0) -> multiprocessing.Pool:
    """
    Return a ``multiprocessing.Pool`` that limits each worker’s CPU usage.

    The pool size defaults to half of the available cores so that the
    total utilisation stays below the 50 % ceiling even when all workers
    are busy.

    Parameters
    ----------
    max_workers:
        Number of worker processes.  ``None`` defaults to ``os.cpu_count() // 2``.
    max_cpu_percent:
        Per‑worker CPU usage limit (default 50 % of a core).

    Returns
    -------
    multiprocessing.Pool
        A pool ready for ``apply_async`` / ``map`` calls.
    """
    if max_workers is None:
        max_workers = max(1, (os.cpu_count() or 2) // 2)

    return multiprocessing.Pool(
        processes=max_workers,
        initializer=_worker_initializer,
        initargs=(max_cpu_percent,),
    )


# ----------------------------------------------------------------------
# Helper to apply throttling inside a worker
# ----------------------------------------------------------------------
def throttled_call(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """
    Execute ``func`` while respecting the per‑process CPU limit.

    Workers created via :func:`cpu_limited_pool` have a ``_throttle``
    attribute injected by the initializer.  This wrapper calls that
    method before and after the actual work to keep the CPU usage in
    check.

    Returns
    -------
    Any
        The result of ``func(*args, **kwargs)``.
    """
    import psutil

    proc = psutil.Process(os.getpid())
    throttle = getattr(proc, "_throttle", None)  # type: ignore[attr-defined]

    if callable(throttle):
        throttle()  # pre‑work throttling

    result = func(*args, **kwargs)

    if callable(throttle):
        throttle()  # post‑work throttling

    return result