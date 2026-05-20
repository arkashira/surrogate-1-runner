"""
GPU discovery, allocation, and hot‑plug event emitter.

The module uses `pynvml` for real hardware discovery when available.
For unit tests a custom discovery function can be injected.
"""

import threading
import time
import uuid
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional

# Try to import pynvml; fall back to a stub if not available.
try:
    import pynvml
except Exception:  # pragma: no cover
    pynvml = None  # type: ignore


@dataclass(frozen=True)
class GPUInfo:
    """Immutable representation of a GPU."""
    id: str  # unique identifier (e.g., index)
    total_memory: int  # bytes
    bandwidth: int  # MB/s
    driver_version: str


class GPUAllocator:
    """
    Manages GPU discovery, allocation, and hot‑plug events.

    Attributes
    ----------
    poll_interval : float
        Seconds between discovery polls.
    discovery_func : Callable[[], Iterable[GPUInfo]]
        Function that returns the current list of GPUs.
    """

    def __init__(
        self,
        poll_interval: float = 1.0,
        discovery_func: Optional[Callable[[], Iterable[GPUInfo]]] = None,
    ):
        self.poll_interval = poll_interval
        self.discovery_func = discovery_func or self._default_discovery
        self._lock = threading.Lock()
        self._reserved: Dict[str, str] = {}  # gpu_id -> handle
        self._prev_gpus: Dict[str, GPUInfo] = {}
        self._listeners: Dict[str, List[Callable[[GPUInfo], None]]] = {
            "gpu_added": [],
            "gpu_removed": [],
        }
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def register_listener(
        self, event_type: str, callback: Callable[[GPUInfo], None]
    ) -> None:
        """Register a callback for a hot‑plug event."""
        if event_type not in self._listeners:
            raise ValueError(f"Unsupported event_type: {event_type}")
        self._listeners[event_type].append(callback)

    def allocate(self, gpu_id: str) -> str:
        """
        Allocate a GPU by ID.

        Returns a deterministic handle (the GPU ID itself).
        Raises RuntimeError if the GPU is already reserved.
        """
        with self._lock:
            if gpu_id in self._reserved:
                raise RuntimeError(f"GPU {gpu_id} is already reserved")
            self._reserved[gpu_id] = gpu_id
            return gpu_id

    def release(self, gpu_id: str) -> None:
        """Release a previously allocated GPU."""
        with self._lock:
            self._reserved.pop(gpu_id, None)

    def get_allocated(self) -> List[GPUInfo]:
        """Return a list of currently allocated GPUs."""
        with self._lock:
            ids = set(self._reserved.keys())
        return [gpu for gpu in self._current_gpus() if gpu.id in ids]

    def get_available(self) -> List[GPUInfo]:
        """Return a list of GPUs that are not reserved."""
        with self._lock:
            reserved = set(self._reserved.keys())
        return [gpu for gpu in self._current_gpus() if gpu.id not in reserved]

    def stop(self) -> None:
        """Stop the background polling thread."""
        self._stop_event.set()
        self._thread.join()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _current_gpus(self) -> List[GPUInfo]:
        """Return the latest discovered GPUs."""
        return list(self.discovery_func())

    def _poll_loop(self) -> None:
        """Background thread that polls for GPU changes."""
        while not self._stop_event.is_set():
            try:
                current = {gpu.id: gpu for gpu in self.discovery_func()}
            except Exception:
                current = {}
            added = [gpu for id_, gpu in current.items() if id_ not in self._prev_gpus]
            removed = [gpu for id_, gpu in self._prev_gpus.items() if id_ not in current]
            for gpu in added:
                for cb in self._listeners["gpu_added"]:
                    cb(gpu)
            for gpu in removed:
                for cb in self._listeners["gpu_removed"]:
                    cb(gpu)
            self._prev_gpus = current
            time.sleep(self.poll_interval)

    # ------------------------------------------------------------------
    # Default discovery implementation
    # ------------------------------------------------------------------
    def _default_discovery(self) -> List[GPUInfo]:
        """Discover GPUs using pynvml."""
        if not pynvml:
            return []

        try:
            pynvml.nvmlInit()
            count = pynvml.nvmlDeviceGetCount()
            gpus: List[GPUInfo] = []
            for idx in range(count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
                mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                pci = pynvml.nvmlDeviceGetPciInfo(handle)
                # Approximate bandwidth: generation * width * 8 (Gbps) * 1000 (Mbps)
                bandwidth = (
                    pci.pciLinkGeneration * pci.pciLinkWidth * 8 * 1000
                ) if pci else 0
                driver = pynvml.nvmlSystemGetDriverVersion()
                gpus.append(
                    GPUInfo(
                        id=str(idx),
                        total_memory=mem.total,
                        bandwidth=bandwidth,
                        driver_version=driver.decode() if isinstance(driver, bytes) else driver,
                    )
                )
        finally:
            if pynvml:
                pynvml.nvmlShutdown()
        return gpus