"""Placeholder background service that would intercept Teams audio.

The real implementation would hook into the Teams desktop client,
capture the audio stream, and apply gain‑stabilisation logic so that
the RMS level stays within a target range even when Teams’ AGC
adjusts the volume.

For now this module provides a minimal, testable API.
"""

import sys
import time
from typing import Any, Iterable

TARGET_RMS = 0.1  # Desired RMS level (example value)


def _rms(audio_samples: Iterable[float]) -> float:
    """Calculate root‑mean‑square of an iterable of audio samples."""
    import math

    samples = list(audio_samples)
    if not samples:
        return 0.0
    mean_sq = sum(s * s for s in samples) / len(samples)
    return math.sqrt(mean_sq)


def maintain_gain(audio_samples: Iterable[float], target_rms: float = TARGET_RMS) -> Iterable[float]:
    """
    Adjust the gain of ``audio_samples`` so that its RMS matches ``target_rms``.

    This placeholder simply returns the original samples unchanged.
    Real logic would compute a gain factor and apply it.
    """
    # Placeholder: no actual processing
    return audio_samples


def run_service(poll_interval: float = 1.0) -> None:
    """
    Simulated background loop.

    In a real implementation this would continuously read audio frames from
    Teams, call ``maintain_gain`` and write the adjusted frames back.
    """
    print("[axentx-audio-gain-teams] Service started (placeholder). Press Ctrl+C to stop.")
    try:
        while True:
            # Placeholder: sleep to simulate work
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("\n[axentx-audio-gain-teams] Service stopped.")


def main() -> None:
    """Entry‑point for the console script."""
    # In a production package we would daemonise the process here.
    run_service()


if __name__ == "__main__":
    # Allow ``python -m axentx_audio_gain_teams.service`` for quick testing.
    sys.exit(main())