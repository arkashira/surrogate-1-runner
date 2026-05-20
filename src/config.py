"""Central configuration for the idle‑resource detector."""

from dataclasses import dataclass
from typing import Mapping

# ----------------------------------------------------------------------
# Thresholds – can be overridden by environment variables or a config file
# ----------------------------------------------------------------------
DEFAULT_IDLE_CPU_PCT = 10.0          # % CPU below which we call a resource idle
DEFAULT_IDLE_HOURS_PCT = 5.0         # % CPU below which we count an hour as idle
DEFAULT_DAYS_BACK = 30              # How many days of history we analyse

# ----------------------------------------------------------------------
# Simplified cost mapping (USD per hour). In a real deployment you would
# pull this from the AWS Pricing API or a maintained CSV.
# ----------------------------------------------------------------------
COST_PER_HOUR: Mapping[str, float] = {
    "t3.micro": 0.0104,
    "t3.small": 0.0208,
    "t3.medium": 0.0416,
    "t3.large": 0.0832,
    # fallback for any type we do not explicitly know
    "default": 0.10,
}