"""
Calculate a battery health score (0–100) from raw metrics.
The formula is intentionally simple so that it can be swapped out later.
"""

from .metrics import get_voltage, get_temperature, get_cycle_count

def _normalize_voltage(v: float) -> float:
    # Assume nominal 3.7 V, healthy range 3.4–4.2 V
    return max(0.0, min(1.0, (v - 3.4) / (4.2 - 3.4)))

def _normalize_temp(t: float) -> float:
    # Assume safe temp 0–45 °C
    return max(0.0, min(1.0, (45 - t) / 45))

def _normalize_cycles(c: int) -> float:
    # Assume 0–500 cycles is healthy
    return max(0.0, min(1.0, (500 - c) / 500))

def get_battery_health_score() -> int:
    """Return an integer score between 0 and 100."""
    v = _normalize_voltage(get_voltage())
    t = _normalize_temp(get_temperature())
    c = _normalize_cycles(get_cycle_count())

    # Weighted sum: 50% voltage, 30% temperature, 20% cycles
    score = 0.5 * v + 0.3 * t + 0.2 * c
    return int(round(score * 100))