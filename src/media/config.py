"""
Configuration constants for media buffering.
"""

# Number of bytes to prefetch before playback starts.
# 5 MB is a good compromise for most local files.
PREBUFFER_BYTES: int = 5 * 1024 * 1024  # 5 MiB

# Maximum number of concurrent prefetch tasks.
MAX_PREFETCH_WORKERS: int = 4

# Timeout for a prefetch operation in seconds.
PREFETCH_TIMEOUT: int = 10

# Optional: expose the same values as a dataclass for the state machine.
from dataclasses import dataclass

@dataclass(frozen=True)
class BufferConfig:
    prebuffer_bytes: int = PREBUFFER_BYTES
    max_workers: int = MAX_PREFETCH_WORKERS
    timeout: int = PREFETCH_TIMEOUT