"""
Centralised configuration for the media buffer.
All values are expressed in bytes unless otherwise noted.
"""

MEDIA_BUFFER_CONFIG = {
    # Default size (1 MiB)
    "buffer_size": 1024 * 1024,

    # Minimum / maximum allowed sizes (0.5 MiB – 10 MiB)
    "min_buffer_size": int(0.5 * 1024 * 1024),
    "max_buffer_size": 10 * 1024 * 1024,

    # When the buffer is at least this fraction full, trigger optimisation
    "optimization_threshold": 0.7,

    # How often (in seconds) to re‑evaluate optimisation
    "optimization_interval": 5,
}