"""
Automatic brightness adjustment module for the media player.

This module exposes a BrightnessAdjuster class that:
  * is enabled by default
  * can be overridden by user settings
  * adjusts brightness based on ambient light sensor data
  * logs adjustments for debugging

The implementation is intentionally lightweight and uses a simple
linear mapping from ambient lux to brightness percentage.
"""

import logging
import time
from typing import Callable, Optional

# Import settings to respect user overrides
from .settings import Settings

log = logging.getLogger(__name__)


class BrightnessAdjuster:
    """
    Adjusts screen brightness automatically based on ambient light.

    Parameters
    ----------
    sensor_reading : Callable[[], float]
        Function that returns the current ambient light level in lux.
    set_brightness : Callable[[float], None]
        Function that sets the screen brightness (0.0 to 1.0).
    poll_interval : float, optional
        Seconds between sensor polls. Default is 5.0.
    """

    def __init__(
        self,
        sensor_reading: Callable[[], float],
        set_brightness: Callable[[float], None],
        poll_interval: float = 5.0,
    ):
        self.sensor_reading = sensor_reading
        self.set_brightness = set_brightness
        self.poll_interval = poll_interval
        self._running = False
        self._thread = None
        self.settings = Settings()

    def _lux_to_brightness(self, lux: float) -> float:
        """
        Map lux to brightness percentage.

        Uses a simple linear mapping:
          - 0 lux -> 0.2 brightness
          - 100 lux -> 0.5 brightness
          - 500 lux -> 0.8 brightness
          - >500 lux -> 1.0 brightness
        """
        if lux <= 0:
            return 0.2
        if lux >= 500:
            return 1.0
        # Linear interpolation between 0.2 and 0.8
        return 0.2 + (lux / 500.0) * 0.6

    def _adjustment_loop(self):
        """Internal loop for continuous brightness adjustment."""
        while self._running:
            try:
                # Check if auto-brightness is enabled
                if not self.settings.auto_brightness_enabled:
                    log.debug("Auto-brightness disabled, skipping adjustment")
                    time.sleep(self.poll_interval)
                    continue

                lux = self.sensor_reading()
                brightness = self._lux_to_brightness(lux)
                
                # Respect user override if set
                if self.settings.user_brightness is not None:
                    brightness = self.settings.user_brightness
                    log.debug("Using user override brightness: %.2f", brightness)
                else:
                    log.debug("Using auto-calculated brightness: %.2f", brightness)
                
                self.set_brightness(brightness)
                log.info(
                    "Ambient lux=%.1f -> brightness=%.2f",
                    lux,
                    brightness
                )
            except Exception as e:
                log.exception("Error in BrightnessAdjuster loop: %s", e)
            time.sleep(self.poll_interval)

    def start(self):
        """Start the automatic brightness adjustment loop."""
        import threading
        
        if self._running:
            log.debug("BrightnessAdjuster already running")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._adjustment_loop, daemon=True)
        self._thread.start()
        log.info("BrightnessAdjuster started")

    def stop(self):
        """Stop the automatic brightness adjustment loop."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=self.poll_interval + 1)
        log.info("BrightnessAdjuster stopped")

    def update_settings(self):
        """Force reload settings from storage."""
        self.settings._load()
        log.info("Settings reloaded")