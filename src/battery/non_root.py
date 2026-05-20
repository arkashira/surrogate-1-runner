"""
Non-root battery monitoring for surrogate-1.

This module provides a secure, cross-platform interface to query battery
status without requiring elevated privileges. Uses the `psutil` library,
which reads from system files that are world-readable on most systems.

No root access required. Falls back gracefully when battery info is unavailable.
"""

import logging
import warnings
from typing import Optional, Dict, Any

try:
    import psutil
except ImportError:
    psutil = None

logger = logging.getLogger(__name__)


def check_battery_available() -> bool:
    """
    Check if battery information is accessible.
    
    Returns:
        bool: True if battery data can be retrieved, False otherwise.
    """
    if psutil is None:
        logger.warning("psutil not installed. Install with: pip install psutil")
        return False
    
    try:
        battery = psutil.sensors_battery()
        return battery is not None
    except Exception as e:
        logger.warning(f"Unable to access battery information: {e}")
        return False


def _battery_percent() -> Optional[float]:
    """Return the current battery percentage, or None if unavailable."""
    if psutil is None:
        return None
    try:
        battery = psutil.sensors_battery()
        return battery.percent if battery else None
    except Exception as e:
        logger.debug(f"Error reading battery percent: {e}")
        return None


def _battery_time_left() -> Optional[int]:
    """Return estimated seconds left until discharge, or None if unavailable."""
    if psutil is None:
        return None
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return None
        if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            return None  # Charging or unlimited
        return battery.secsleft
    except Exception as e:
        logger.debug(f"Error reading battery time: {e}")
        return None


def _battery_plugged() -> Optional[bool]:
    """Return True if plugged in, False if on battery, or None if unknown."""
    if psutil is None:
        return None
    try:
        battery = psutil.sensors_battery()
        return battery.power_plugged if battery else None
    except Exception as e:
        logger.debug(f"Error reading power status: {e}")
        return None


def get_battery_info() -> Dict[str, Any]:
    """
    Retrieve battery information in a non-root friendly format.
    
    Returns:
        dict: Contains 'percent', 'time_left_sec', 'plugged_in' keys.
              Values are None if unavailable.
    """
    return {
        "percent": _battery_percent(),
        "time_left_sec": _battery_time_left(),
        "plugged_in": _battery_plugged(),
    }


# =============================================================================
# Stubs for root-dependent functions (API compatibility)
# =============================================================================

def set_battery_thresholds(*args, **kwargs) -> None:
    """
    Set battery thresholds (requires root).
    
    Warning: This function requires elevated privileges and is not
    available in non-root mode.
    """
    warnings.warn(
        "set_battery_thresholds() requires root privileges and is "
        "not available in non-root mode.",
        RuntimeWarning,
        stacklevel=2
    )
    logger.debug("Stub called: set_battery_thresholds")


def enable_battery_notifications(*args, **kwargs) -> None:
    """
    Enable battery notifications (requires root).
    
    Warning: This function requires elevated privileges and is not
    available in non-root mode.
    """
    warnings.warn(
        "enable_battery_notifications() requires root privileges and is "
        "not available in non-root mode.",
        RuntimeWarning,
        stacklevel=2
    )
    logger.debug("Stub called: enable_battery_notifications")