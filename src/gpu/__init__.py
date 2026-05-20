"""
GPU discovery and allocation module for the surrogate-1 SDK.

Provides:
- :func:`list_gpus` – enumerate all GPUs with details.
- :func:`allocate_gpu` – reserve a GPU, returning its ID.
- :func:`release_gpu` – free a previously allocated GPU.
- :func:`register_hotplug_callback` – register a callback for GPU hot‑plug events.
"""

from __future__ import annotations

from .discovery import (
    GPUInfo,
    list_gpus,
    allocate_gpu,
    release_gpu,
    register_hotplug_callback,
    HotplugEvent,
)

__all__ = [
    "GPUInfo",
    "HotplugEvent",
    "list_gpus",
    "allocate_gpu",
    "release_gpu",
    "register_hotplug_callback",
]