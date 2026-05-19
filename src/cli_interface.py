"""
BatteryGuard CLI Interface.

Provides utilities to fetch battery metrics, generate alerts, and format output.
"""

from __future__ import annotations

import os
import pathlib
from typing import Any, Dict, Optional

import psutil


def _read_linux_temperature() -> Optional[int]:
    """
    Attempt to read battery temperature from common sysfs locations (Linux only).
    Returns temperature in Celsius or None if unavailable.
    """
    # Check common paths for BAT0. 
    # Note: Some systems use BAT1, this can be extended later.
    possible_paths = [
        "/sys/class/power_supply/BAT0/temp",
        "/sys/class/power_supply/BAT0/temperature",
    ]

    for path_str in possible_paths:
        path = pathlib.Path(path_str)
        if path.is_file():
            try:
                # Kernel often exposes temp in millidegrees Celsius.
                raw = int(path.read_text().strip())
                return raw // 1000 if raw > 1000 else raw
            except (ValueError, OSError):
                continue
    return None


def get_battery_metrics() -> Dict[str, Any]:
    """
    Gather current battery metrics.

    Returns:
        Dictionary containing percent, secsleft, power_plugged, and temperature.
    """
    battery = psutil.sensors_battery()
    
    if battery is None:
        return {
            "percent": None,
            "secsleft": None,
            "power_plugged": None,
            "temperature": None,
        }

    metrics = {
        "percent": battery.percent,
        "secsleft": battery.secsleft,
        "power_plugged": battery.power_plugged,
        "temperature": None,
    }

    # Temperature is Linux-specific
    if os.name == "posix":
        metrics["temperature"] = _read_linux_temperature()

    return metrics


def generate_alerts(metrics: Dict[str, Any]) -> list[str]:
    """
    Generate alerts based on battery metrics.

    Args:
        metrics: Dictionary returned by get_battery_metrics.

    Returns:
        List of alert strings.
    """
    alerts = []
    percent = metrics.get("percent")
    plugged = metrics.get("power_plugged")

    if percent is None or plugged is None:
        return ["Unable to determine battery status."]

    # Low battery alert
    if not plugged and percent <= 20:
        alerts.append(f"⚠️ Battery low ({percent:.0f}%). Plug in the charger.")

    # Critical battery alert
    if not plugged and percent <= 10:
        alerts.append(f"🔴 Critical battery level ({percent:.0f}%)! Save your work!")

    # Full charge alert
    if plugged and percent >= 95:
        alerts.append(f"🔌 Battery sufficiently charged ({percent:.0f}%). You may unplug the charger.")

    return alerts


def print_battery_metrics(metrics: Dict[str, Any]) -> None:
    """
    Formats and prints battery metrics and alerts to stdout.
    """
    if metrics["percent"] is None:
        print("No battery detected or data unavailable.")
        return

    # 1. Print Core Metrics
    print(f"Battery: {metrics['percent']}%")
    print(f"Status: {'Power Plugged' if metrics['power_plugged'] else 'On Battery'}")

    # 2. Format Time Remaining
    secs = metrics["secsleft"]
    if secs == psutil.POWER_TIME_UNKNOWN or secs < 0:
        # psutil returns -1 for unknown, sometimes positive for charging time
        # If plugged in and time is unknown or negative, it usually means "calculating" or "unlimited"
        time_str = "Calculating..." if metrics["power_plugged"] else "Unknown"
    else:
        hours = int(secs // 3600)
        minutes = int((secs % 3600) // 60)
        time_str = f"{hours}h {minutes}m"
    
    print(f"Time Remaining: {time_str}")

    # 3. Print Temperature if available
    temp = metrics.get("temperature")
    if temp is not None:
        print(f"Temperature: {temp}°C")

    # 4. Print Alerts
    alerts = generate_alerts(metrics)
    if alerts:
        print("\n--- Alerts ---")
        for alert in alerts:
            print(f"• {alert}")