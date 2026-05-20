"""
Resource usage metrics collection for parallel test analysis.

This module provides a lightweight context manager that records CPU and
memory usage before and after a block of code. The metrics are returned
as a dictionary and can be logged or sent to a monitoring backend.

The implementation uses the `psutil` library, which is already a
dependency of the surrogate-1 project. If `psutil` is not available,
the module falls back to a no‑op implementation that returns zeros.
"""

import time
from contextlib import contextmanager
from typing import Dict, Optional

try:
    import psutil  # type: ignore
except ImportError:  # pragma: no cover
    psutil = None  # type: ignore


def _get_process() -> Optional[psutil.Process]:
    """Return the current process or None if psutil is unavailable."""
    if psutil is None:
        return None
    return psutil.Process()


def _snapshot() -> Dict[str, float]:
    """
    Capture a snapshot of CPU percent and memory usage.

    Returns:
        dict: {
            "cpu_percent": float,  # percent of CPU used by this process
            "memory_rss": float,   # resident set size in MB
            "memory_vms": float,   # virtual memory size in MB
        }
    """
    proc = _get_process()
    if proc is None:
        return {
            "cpu_percent": 0.0,
            "memory_rss": 0.0,
            "memory_vms": 0.0,
        }

    # psutil.cpu_percent() with interval=0.0 returns the last known value
    cpu = proc.cpu_percent(interval=0.0)
    mem = proc.memory_info()
    return {
        "cpu_percent": cpu,
        "memory_rss": mem.rss / (1024 * 1024),
        "memory_vms": mem.vms / (1024 * 1024),
    }


@contextmanager
def monitor_resource_usage() -> Dict[str, float]:
    """
    Context manager that measures CPU and memory usage around a block.

    Usage:
        with monitor_resource_usage() as metrics:
            # code to monitor
        print(metrics)  # contains before/after snapshots and deltas

    Returns:
        dict: {
            "before": {...},
            "after": {...},
            "delta_cpu_percent": float,
            "delta_memory_rss": float,
            "delta_memory_vms": float,
        }
    """
    before = _snapshot()
    # Small sleep to allow psutil to update CPU percent
    time.sleep(0.1)
    yield before
    after = _snapshot()
    delta_cpu = after["cpu_percent"] - before["cpu_percent"]
    delta_mem_rss = after["memory_rss"] - before["memory_rss"]
    delta_mem_vms = after["memory_vms"] - before["memory_vms"]
    return {
        "before": before,
        "after": after,
        "delta_cpu_percent": delta_cpu,
        "delta_memory_rss": delta_mem_rss,
        "delta_memory_vms": delta_mem_vms,
    }


def log_metrics(name: str, metrics: Dict[str, float]) -> None:
    """
    Log the collected metrics to stdout.

    Args:
        name: Identifier for the monitored block.
        metrics: Dictionary returned by `monitor_resource_usage`.
    """
    print(f"[metrics] {name}")
    print(f"  CPU percent before: {metrics['before']['cpu_percent']:.2f}%")
    print(f"  CPU percent after:  {metrics['after']['cpu_percent']:.2f}%")
    print(f"  CPU delta:          {metrics['delta_cpu_percent']:.2f}%")
    print(f"  RSS before:         {metrics['before']['memory_rss']:.2f} MB")
    print(f"  RSS after:          {metrics['after']['memory_rss']:.2f} MB")
    print(f"  RSS delta:          {metrics['delta_memory_rss']:.2f} MB")
    print(f"  VMS before:         {metrics['before']['memory_vms']:.2f} MB")
    print(f"  VMS after:          {metrics['after']['memory_vms']:.2f} MB")
    print(f"  VMS delta:          {metrics['delta_memory_vms']:.2f} MB")