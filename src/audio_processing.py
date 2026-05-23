import numpy as np
from typing import Optional

class AudioProcessor:
    def __init__(self):
        self.gain_boost_enabled = False
        self.gain_boost_factor = 2.0  # Default gain boost factor

    def apply_gain_boost(self, audio_data: np.ndarray) -> np.ndarray:
        """Apply gain boost to audio data if enabled."""
        if self.gain_boost_enabled:
            return audio_data * self.gain_boost_factor
        return audio_data

    def toggle_gain_boost(self, enable: bool) -> None:
        """Toggle the gain boost feature."""
        self.gain_boost_enabled = enable

    def set_gain_boost_factor(self, factor: float) -> None:
        """Set the gain boost factor."""
        self.gain_boost_factor = factor