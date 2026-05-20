"""
Resource monitoring and throttling utilities for the surrogate integration tool.

This module provides a lightweight, cross‑platform monitor that can be attached
to any subprocess (e.g. the Freerouter process started by the KiCAD integration
tool).  It periodically samples CPU and memory usage and can:

* Emit user‑visible feedback via a callback.
* Lower the process priority to keep KiCAD responsive.
* Optionally terminate the process if it exceeds configurable thresholds.

The monitor runs in a background thread so it does not block the main
integration logic.  It is intentionally simple to keep startup time low
and avoid adding heavy dependencies to the KiCAD runtime.
"""

import os
import time
import threading
import logging
from typing import Callable, Optional

try:
    import psutil  # type: ignore
except ImportError:
    psutil = None  # pragma: no cover

# Configure a module‑level logger.  The integration tool can redirect this
# to its own UI or console.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ResourceMonitor:
    """
    Monitor CPU and memory usage of a target process.

    Parameters
    ----------
    pid : int
        Process ID of the target subprocess.
    callback : Callable[[str], None]
        Function called with a human‑readable status message.
    interval : float, optional
        Seconds between samples.  Default is 1.0.
    max_cpu : float, optional
        Maximum allowed CPU usage in percent.  If exceeded, the process
        will be terminated.  Default is 50.0.
    max_mem : int, optional
        Maximum allowed memory usage in bytes.  If exceeded, the process
        will be terminated.  Default is 200 MiB.
    low_priority : bool, optional
        If True, the monitor will lower the process priority to keep KiCAD
        responsive.  Default is True.
    """

    def __init__(
        self,
        pid: int,
        callback: Callable[[str], None],
        interval: float = 1.0,
        max_cpu: float = 50.0,
        max_mem: int = 200 * 1024 * 1024,
        low_priority: bool = True,
    ):
        if psutil is None:
            raise RuntimeError("psutil is required for ResourceMonitor")

        self.pid = pid
        self.callback = callback
        self.interval = interval
        self.max_cpu = max_cpu
        self.max_mem = max_mem
        self.low_priority = low_priority

        self._proc = psutil.Process(pid)
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _set_low_priority(self):
        """Lower the process priority to keep KiCAD responsive."""
        try:
            if os.name == "nt":
                # Windows: set priority to BELOW_NORMAL
                self._proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            else:
                # Unix: set nice value to +10
                self._proc.nice(10)
            logger.debug("Set low priority for PID %s", self.pid)
        except Exception as exc:
            logger.warning("Failed to set low priority for PID %s: %s", self.pid, exc)

    def _monitor_loop(self):
        """Background thread that samples resource usage."""
        self._set_low_priority()
        while not self._stop_event.is_set():
            try:
                cpu = self._proc.cpu_percent(interval=None)
                mem = self._proc.memory_info().rss
                status = f"Freerouter PID {self.pid} - CPU: {cpu:.1f}% | MEM: {mem / (1024 * 1024):.1f} MiB"
                self.callback(status)

                if cpu > self.max_cpu:
                    self.callback(f"CPU usage {cpu:.1f}% exceeded threshold {self.max_cpu}%; terminating.")
                    self._proc.terminate()
                    break

                if mem > self.max_mem:
                    self.callback(f"Memory usage {mem / (1024 * 1024):.1f} MiB exceeded threshold {self.max_mem / (1024 * 1024):.1f} MiB; terminating.")
                    self._proc.terminate()
                    break

                time.sleep(self.interval)
            except psutil.NoSuchProcess:
                self.callback(f"Process PID {self.pid} terminated.")
                break
            except Exception as exc:
                self.callback(f"Monitoring error: {exc}")
                break

    def start(self):
        """Start the monitoring thread."""
        if self._thread and self._thread.is_alive():
            logger.debug("Monitor already running for PID %s", self.pid)
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        logger.debug("Started resource monitor for PID %s", self.pid)

    def stop(self):
        """Signal the monitoring thread to exit."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        logger.debug("Stopped resource monitor for PID %s", self.pid)


def monitor_process(
    pid: int,
    callback: Callable[[str], None],
    *,
    interval: float = 1.0,
    max_cpu: float = 50.0,
    max_mem: int = 200 * 1024 * 1024,
    low_priority: bool = True,
) -> ResourceMonitor:
    """
    Convenience wrapper that creates and starts a ResourceMonitor.

    Returns the monitor instance so the caller can stop it later.
    """
    monitor = ResourceMonitor(
        pid,
        callback,
        interval=interval,
        max_cpu=max_cpu,
        max_mem=max_mem,
        low_priority=low_priority,
    )
    monitor.start()
    return monitor