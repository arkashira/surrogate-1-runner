import pytest
from axentx_audio_gain_teams import service


def test_rms_calculation():
    # RMS of [0, 0, 0] should be 0
    assert service._rms([0, 0, 0]) == pytest.approx(0.0)

    # RMS of [1, -1] should be 1
    assert service._rms([1, -1]) == pytest.approx(1.0)

    # RMS of [0.5, 0.5] should be 0.5
    assert service._rms([0.5, 0.5]) == pytest.approx(0.5)


def test_maintain_gain_returns_input_unchanged():
    samples = [0.1, -0.2, 0.3, -0.4]
    result = list(service.maintain_gain(samples, target_rms=0.2))
    assert result == samples