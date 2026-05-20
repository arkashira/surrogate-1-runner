"""
Charge limit policy implementation for battery management.

This module provides:
  * `ChargeLimitPolicy` dataclass – holds configuration.
  * `load_policy_from_file` – load policy from JSON.
  * `enforce_policy` – monitor battery level and stop charging when threshold is reached.
  * `display_policy` – user-friendly display of current policy.

The implementation is intentionally lightweight and platform‑agnostic:
  * On Linux it writes to the sysfs charge control file if available.
  * On macOS it uses `pmset` to disable the charger.
  * If neither method is available, it falls back to a no‑op with a warning.
"""

import json
import os
import sys
import time
import psutil
import subprocess
from dataclasses import dataclass
from typing import Optional

@dataclass
class ChargeLimitPolicy:
    """
    Configuration for charge‑limit policy.
    """
    threshold_percent: int  # e.g., 80 for 80%
    check_interval_sec: int = 60  # how often to check battery level
    enabled: bool = True

    def __post_init__(self):
        if not (0 < self.threshold_percent <= 100):
            raise ValueError("threshold_percent must be between 1 and 100")
        if self.check_interval_sec <= 0:
            raise ValueError("check_interval_sec must be positive")

def load_policy_from_file(path: str) -> ChargeLimitPolicy:
    """
    Load a ChargeLimitPolicy from a JSON file.

    Expected JSON format:
    {
        "threshold_percent": 80,
        "check_interval_sec": 60,
        "enabled": true
    }
    """
    with open(path, "r") as f:
        data = json.load(f)
    return ChargeLimitPolicy(**data)

def _stop_charging_linux() -> bool:
    """
    Attempt to stop charging on Linux by writing to the sysfs charge control file.
    Returns True if successful, False otherwise.
    """
    # Common path for battery charge control
    sysfs_paths = [
        "/sys/class/power_supply/BAT0/charge_control_end_threshold",
        "/sys/class/power_supply/BAT1/charge_control_end_threshold",
    ]
    for path in sysfs_paths:
        if os.path.exists(path):
            try:
                with open(path, "w") as f:
                    f.write("0\n")  # 0 disables charging
                return True
            except Exception as e:
                print(f"[WARN] Failed to write to {path}: {e}", file=sys.stderr)
    return False

def _stop_charging_macos() -> bool:
    """
    Attempt to stop charging on macOS using pmset.
    Returns True if successful, False otherwise.
    """
    try:
        # pmset -a charger 0 disables the charger
        subprocess.run(["pmset", "-a", "charger", "0"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"[WARN] pmset failed: {e}", file=sys.stderr)
        return False

def _stop_charging() -> bool:
    """
    Platform‑agnostic wrapper to stop charging.
    """
    if sys.platform.startswith("linux"):
        return _stop_charging_linux()
    elif sys.platform == "darwin":
        return _stop_charging_macos()
    else:
        print("[WARN] Unsupported platform for stopping charging", file=sys.stderr)
        return False

def enforce_policy(policy: ChargeLimitPolicy, stop_charging_func=_stop_charging) -> None:
    """
    Enforce the given charge‑limit policy in real‑time.

    This function runs an infinite loop checking the battery level
    every `policy.check_interval_sec` seconds. If the battery level
    reaches or exceeds `policy.threshold_percent`, it attempts to
    stop charging via the platform‑specific method.
    """
    if not policy.enabled:
        print("[INFO] Charge limit policy is disabled.")
        return

    print(f"[INFO] Enforcing charge limit: {policy.threshold_percent}% threshold, "
          f"check interval {policy.check_interval_sec}s")

    while True:
        battery = psutil.sensors_battery()
        if battery is None:
            print("[WARN] No battery information available.", file=sys.stderr)
            time.sleep(policy.check_interval_sec)
            continue

        percent = battery.percent
        print(f"[DEBUG] Battery level: {percent}%")

        if percent >= policy.threshold_percent:
            print(f"[INFO] Battery level {percent}% >= threshold {policy.threshold_percent}%. "
                  "Attempting to stop charging.")
            if stop_charging_func():
                print("[INFO] Charging stopped successfully.")
            else:
                print("[WARN] Failed to stop charging.")
            # Once stopped, break out of loop
            break

        time.sleep(policy.check_interval_sec)

def display_policy(policy: ChargeLimitPolicy) -> None:
    """
    Print the current policy in a user‑friendly format.
    """
    status = "ENABLED" if policy.enabled else "DISABLED"
    print(f"Charge‑Limit Policy [{status}]:")
    print(f"  Threshold: {policy.threshold_percent}%")
    print(f"  Check Interval: {policy.check_interval_sec}s")

# If this module is executed directly, load policy from a default config
# and start enforcement. This is optional and can be removed if not needed.
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Charge‑limit policy enforcement")
    parser.add_argument(
        "--config",
        type=str,
        default="charge_limit_policy.json",
        help="Path to JSON config file",
    )
    args = parser.parse_args()

    try:
        policy = load_policy_from_file(args.config)
    except Exception as e:
        print(f"[ERROR] Failed to load policy: {e}", file=sys.stderr)
        sys.exit(1)

    display_policy(policy)
    enforce_policy(policy)