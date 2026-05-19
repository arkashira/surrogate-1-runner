"""
BatteryGuard health-score implementation.

Provides a CLI entry point `batteryguard status` that prints a one-line
health score (0-100) with colour coding, the last-updated timestamp, and a
single-sentence recommendation.

The score is calculated from collected battery metrics using a simple
weighted formula. The module is deliberately self-contained so it can be
imported by the existing CLI wrapper without further changes.
"""

from __future__ import annotations

import sys
import datetime
from typing import Dict, Any

# Colour handling – works on Windows and POSIX terminals
try:
    from colorama import init as _colorama_init, Fore, Style
    _colorama_init(autoreset=True)
except ImportError:  # pragma: no cover
    # Fallback: no colour support
    class _NoColor:
        RESET_ALL = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
    Fore = Style = _NoColor()  # type: ignore


# --------------------------------------------------------------------------- #
# Metric weighting configuration
# --------------------------------------------------------------------------- #
WEIGHTS: Dict[str, float] = {
    "capacity_percent": 0.40,   # remaining capacity (0-100 %)
    "cycle_count": 0.20,        # normalized cycles (lower is better)
    "temperature_c": 0.20,      # normalized temperature (ideal ~25 °C)
    "voltage_v": 0.20,          # normalized voltage (ideal ~3.7 V)
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _normalize_capacity(capacity_percent: float) -> float:
    """Normalize capacity to a 0-1 scale."""
    return max(0.0, min(capacity_percent / 100.0, 1.0))

def _normalize_cycle_count(cycle_count: int, max_cycles: int = 1000) -> float:
    """Normalize cycle count where fewer cycles are better."""
    return max(0.0, min(1.0 - (cycle_count / max_cycles), 1.0))

def _normalize_temperature(temp_c: float, ideal: float = 25.0, tolerance: float = 15.0) -> float:
    """Normalize temperature based on deviation from ideal."""
    diff = abs(temp_c - ideal)
    if diff > tolerance:
        return 0.0
    return max(0.0, min(1.0 - (diff / tolerance), 1.0))

def _normalize_voltage(voltage_v: float, ideal: float = 3.7, tolerance: float = 0.5) -> float:
    """Normalize voltage based on deviation from ideal."""
    diff = abs(voltage_v - ideal)
    if diff > tolerance:
        return 0.0
    return max(0.0, min(1.0 - (diff / tolerance), 1.0))

def compute_score(metrics: Dict[str, Any]) -> int:
    """Compute a health score (0-100) from battery metrics."""
    capacity = _normalize_capacity(metrics.get("capacity_percent", 0.0))
    cycles = _normalize_cycle_count(metrics.get("cycle_count", 1_000_000))
    temperature = _normalize_temperature(metrics.get("temperature_c", 100.0))
    voltage = _normalize_voltage(metrics.get("voltage_v", 0.0))

    score = (
        capacity * WEIGHTS["capacity_percent"] +
        cycles * WEIGHTS["cycle_count"] +
        temperature * WEIGHTS["temperature_c"] +
        voltage * WEIGHTS["voltage_v"]
    )
    return int(round(score * 100))

def _colourise_score(score: int) -> str:
    """Return the score string wrapped in ANSI colour codes."""
    if score >= 80:
        colour = Fore.GREEN
    elif score >= 50:
        colour = Fore.YELLOW
    else:
        colour = Fore.RED
    return f"{colour}{score}{Style.RESET_ALL}"

def recommendation(score: int) -> str:
    """Generate a one-sentence recommendation based on the health score."""
    if score >= 80:
        return "Battery health is excellent."
    elif score >= 50:
        return "Battery health is moderate; monitor regularly."
    else:
        return "Battery health is poor; consider replacement soon."

def _load_metrics() -> Dict[str, Any]:
    """Load metrics from the sibling `metrics` module if present."""
    try:
        from . import metrics  # type: ignore
        return metrics.collect_metrics()
    except Exception as exc:
        raise RuntimeError(f"Failed to collect battery metrics: {exc}") from exc

def status() -> None:
    """CLI entry point for `batteryguard status`."""
    try:
        metrics = _load_metrics()
        score = compute_score(metrics)
        ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        line = (
            f"Health Score: {_colourise_score(score)} | "
            f"Updated: {ts} | "
            f"Recommendation: {recommendation(score)}"
        )
        print(line)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    status()