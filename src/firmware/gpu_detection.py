"""
GPU detection and logical device abstraction for the surrogate-1 firmware.

This module provides a minimal yet robust interface for detecting all NVIDIA
GPUs present on the system at boot time and exposing a single logical device
to the operating system.  The implementation relies on the ``nvidia-smi``
utility, which is the standard way to query NVIDIA hardware from user space.
If ``nvidia-smi`` is not available or no GPUs are detected, the module
gracefully falls back to an empty list and a dummy logical device.

The logical device is represented by :class:`LogicalGPU`, which aggregates
the underlying physical GPU identifiers.  The class exposes a small API
that can be extended by the firmware to expose the device to the OS
(e.g. via sysfs, udev rules, or a custom driver interface).

Author: axentx firmware team
"""

import subprocess
import re
from dataclasses import dataclass
from typing import List, Optional


def _run_nvidia_smi() -> Optional[str]:
    """
    Execute ``nvidia-smi -L`` to list GPUs.

    Returns the raw stdout string if the command succeeds, otherwise
    ``None``.
    """
    try:
        result = subprocess.run(
            ["nvidia-smi", "-L"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def detect_gpus() -> List[int]:
    """
    Detect all NVIDIA GPUs on the system.

    Returns:
        A list of GPU indices (0‑based) that were found.  The order
        corresponds to the order reported by ``nvidia-smi``.
    """
    output = _run_nvidia_smi()
    if not output:
        return []

    gpu_ids: List[int] = []
    # ``nvidia-smi -L`` outputs lines like:
    #   GPU 0: Tesla V100-SXM2-16GB (UUID: GPU-xxxx)
    for line in output.splitlines():
        match = re.match(r"GPU\s+(\d+):", line)
        if match:
            gpu_ids.append(int(match.group(1)))
    return gpu_ids


@dataclass
class LogicalGPU:
    """
    Represents a single logical GPU device that aggregates multiple physical GPUs.

    Attributes:
        gpu_ids: List of physical GPU indices that compose this logical device.
    """

    gpu_ids: List[int]

    def __post_init__(self):
        if not self.gpu_ids:
            raise ValueError("LogicalGPU must aggregate at least one physical GPU")

    @property
    def device_name(self) -> str:
        """
        Return a human‑readable name for the logical device.
        """
        return f"axentx-gpu-{self.gpu_ids[0]}"

    def expose_to_os(self) -> None:
        """
        Stub for exposing the logical device to the OS.

        In a real firmware environment this would create a device node,
        register with udev, or interact with a kernel driver.  For the
        purposes of this repository, we simply log the action.
        """
        # Logging is intentionally minimal to avoid external dependencies.
        print(f"[firmware] Exposing logical GPU {self.device_name} with "
              f"physicals {self.gpu_ids}")


def create_logical_gpu() -> Optional[LogicalGPU]:
    """
    Detect GPUs and create a single logical GPU device.

    Returns:
        A :class:`LogicalGPU` instance if at least one GPU was found,
        otherwise ``None``.
    """
    gpu_ids = detect_gpus()
    if not gpu_ids:
        return None
    return LogicalGPU(gpu_ids=gpu_ids)