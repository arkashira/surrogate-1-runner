import os
from pathlib import Path

# ----------------------------------------------------------------------
# Telemetry
# ----------------------------------------------------------------------
TELEMETRY_DIR = Path(
    os.getenv("AXENTX_TELEMETRY_DIR", "/var/log/axentx/telemetry")
)
TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

PERF_LOG_REPORT_INTERVAL = float(
    os.getenv("PERF_LOG_REPORT_INTERVAL", "60")  # seconds
)

# ----------------------------------------------------------------------
# Throttling
# ----------------------------------------------------------------------
THROTTLE_REFRESH_HZ = int(os.getenv("AXENTX_THROTTLE_REFRESH_HZ", "120"))
THROTTLE_FACTOR = float(os.getenv("AXENTX_THROTTLE_FACTOR", "0.5"))  # 0‑1 scale