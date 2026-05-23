"""
Memory profiling utility for surrogate‑1 regression tests.

The script runs a target callable (specified as ``module:function``) while
tracking memory usage with ``tracemalloc`` and ``psutil``.  After the call
completes it forces a garbage‑collection pass, reports the peak memory
consumption and exits with a non‑zero status if the peak exceeds a
user‑specified limit.

Typical usage from a test suite::

    python -m scripts.profile_memory mypackage.parser:parse_stream \
        --input data/large_stream.bin \
        --max-peak-mb 200

The ``--max-peak-mb`` argument is optional; when omitted the script only
reports the measured value.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import traceback
import gc
import time
from typing import Callable, List, Tuple, Any

import psutil
import tracemalloc


def _load_callable(spec: str) -> Callable:
    """
    Load a callable given a ``module:function`` specification.
    """
    if ":" not in spec:
        raise ValueError(
            f"Invalid callable specification '{spec}'. Expected format 'module:function'."
        )
    module_name, func_name = spec.split(":", 1)
    module = importlib.import_module(module_name)
    try:
        func = getattr(module, func_name)
    except AttributeError as exc:
        raise AttributeError(
            f"Module '{module_name}' has no attribute '{func_name}'."
        ) from exc
    if not callable(func):
        raise TypeError(f"'{func_name}' in module '{module_name}' is not callable.")
    return func


def _parse_extra_args(extra: List[str]) -> Tuple[List[Any], dict]:
    """
    Convert a list of ``key=value`` strings into positional and keyword arguments.
    Positional arguments are supplied as plain strings; keyword arguments are
    parsed as JSON values when possible.
    """
    args: List[Any] = []
    kwargs: dict = {}
    for item in extra:
        if "=" in item:
            k, v = item.split("=", 1)
            try:
                # Try to interpret as JSON (e.g. numbers, booleans, lists)
                parsed = json.loads(v)
            except json.JSONDecodeError:
                parsed = v
            kwargs[k] = parsed
        else:
            args.append(item)
    return args, kwargs


def profile_memory(
    target: Callable,
    *args,
    max_peak_mb: float | None = None,
    **kwargs,
) -> float:
    """
    Execute ``target`` while measuring memory usage.

    Returns
    -------
    peak_mb : float
        The peak memory usage observed during execution, expressed in megabytes.
    """
    # Start tracing memory allocations.
    tracemalloc.start()
    process = psutil.Process(os.getpid())

    # Record baseline RSS (resident set size) before execution.
    baseline_rss = process.memory_info().rss

    # Run the target.
    start_time = time.time()
    try:
        target(*args, **kwargs)
    finally:
        # Ensure we stop tracing even if the target raises.
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    # Force a full GC to release any lingering references.
    gc.collect()

    # Measure RSS after GC.
    final_rss = process.memory_info().rss

    # Compute peak memory as the larger of traced peak and RSS delta.
    traced_peak_mb = peak / (1024 * 1024)
    rss_peak_mb = (final_rss - baseline_rss) / (1024 * 1024)
    peak_mb = max(traced_peak_mb, rss_peak_mb)

    # Optional enforcement.
    if max_peak_mb is not None and peak_mb > max_peak_mb:
        raise MemoryError(
            f"Peak memory {peak_mb:.2f} MiB exceeds limit of {max_peak_mb:.2f} MiB."
        )

    duration = time.time() - start_time
    print(
        json.dumps(
            {
                "peak_mb": round(peak_mb, 2),
                "duration_s": round(duration, 2),
                "baseline_rss_mb": round(baseline_rss / (1024 * 1024), 2),
                "final_rss_mb": round(final_rss / (1024 * 1024), 2),
            }
        )
    )
    return peak_mb


def _main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a callable while profiling its memory usage."
    )
    parser.add_argument(
        "callable",
        help="Target to execute, in the form 'module:function'.",
    )
    parser.add_argument(
        "--max-peak-mb",
        type=float,
        default=None,
        help="Fail if peak memory exceeds this value (MiB).",
    )
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Additional arguments passed to the target. "
        "Use key=value for keyword args; plain strings become positional args.",
    )
    args = parser.parse_args()

    try:
        target = _load_callable(args.callable)
        pos_args, kw_args = _parse_extra_args(args.extra)
        profile_memory(
            target,
            *pos_args,
            max_peak_mb=args.max_peak_mb,
            **kw_args,
        )
    except Exception as exc:
        # Print a JSON error payload for easy consumption by CI.
        err = {
            "error": str(exc),
            "type": type(exc).__name__,
            "traceback": traceback.format_exc(),
        }
        print(json.dumps(err), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _main()