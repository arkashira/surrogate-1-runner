"""
Collect raw battery metrics.  Replace the stub implementations with real
system calls or API requests once the data source is known.
"""

def get_voltage() -> float:
    """Return the current battery voltage in volts."""
    # TODO: read from /sys/class/power_supply/BAT0/voltage_now
    return 3.7

def get_temperature() -> float:
    """Return the battery temperature in °C."""
    # TODO: read from /sys/class/power_supply/BAT0/temp
    return 35.0

def get_cycle_count() -> int:
    """Return the number of charge/discharge cycles."""
    # TODO: read from /sys/class/power_supply/BAT0/cycle_count
    return 120