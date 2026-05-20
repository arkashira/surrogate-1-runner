import logging
import time
from typing import Any

import pytest
import torch

# The project is expected to expose a transfer function that moves tensors
# between GPUs.  The function should accept a source device, a destination
# device, and a tensor, and return a non‑blocking handle (e.g. a
# torch.cuda.Event) that can be waited on.  If NVLink is unavailable the
# function should fall back to PCIe and emit a warning.
try:
    from axentx.surrogate import transfer_tensor
except Exception:  # pragma: no cover
    # If the function is not present, the tests will fail loudly.
    transfer_tensor = None  # type: ignore


@pytest.fixture(scope="module")
def available_gpus():
    """Return a list of CUDA device indices if at least two GPUs are present."""
    if torch.cuda.is_available() and torch.cuda.device_count() >= 2:
        return list(range(torch.cuda.device_count()))
    pytest.skip("Test requires at least two CUDA GPUs.")


def _measure_latency_and_bandwidth(
    src: int, dst: int, size_bytes: int, stream: torch.cuda.Stream
) -> tuple[float, float]:
    """
    Transfer a tensor of `size_bytes` from `src` to `dst` using the
    project's `transfer_tensor` function and measure latency and bandwidth.

    Returns:
        latency_us: Latency in microseconds.
        bandwidth_gb_s: Bandwidth in GiB/s.
    """
    # Create a dummy tensor on the source device
    with torch.cuda.device(src):
        tensor = torch.randn(size_bytes // 4, dtype=torch.float32, device="cuda")

    # Create events for timing
    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)

    # Record start
    start_event.record(stream)

    # Perform the transfer
    handle = transfer_tensor(src, dst, tensor)

    # Record end
    end_event.record(stream)

    # Wait for completion
    stream.synchronize()

    # Compute elapsed time in milliseconds
    elapsed_ms = start_event.elapsed_time(end_event)
    latency_us = elapsed_ms * 1_000  # convert ms to µs

    # Bandwidth in GiB/s
    bandwidth_gb_s = (size_bytes / (1024**3)) / (elapsed_ms / 1000)

    return latency_us, bandwidth_gb_s


def test_transfer_latency_and_bandwidth(available_gpus):
    """Verify latency and bandwidth meet the acceptance criteria."""
    src, dst = available_gpus[0], available_gpus[1]
    stream = torch.cuda.Stream()

    # 1 MiB transfer latency test
    latency_us, _ = _measure_latency_and_bandwidth(
        src, dst, size_bytes=1 * 1024 * 1024, stream=stream
    )
    assert (
        latency_us <= 5
    ), f"1 MiB transfer latency {latency_us:.2f} µs exceeds 5 µs threshold"

    # 10 MiB transfer bandwidth test
    _, bandwidth_gb_s = _measure_latency_and_bandwidth(
        src, dst, size_bytes=10 * 1024 * 1024, stream=stream
    )
    # Theoretical peak for NVLink 2.0 is ~25 GiB/s, PCIe 4.0 ~16 GiB/s.
    # We use 25 GiB/s as the reference peak.
    theoretical_peak_gb_s = 25.0
    assert (
        bandwidth_gb_s >= 0.8 * theoretical_peak_gb_s
    ), f"10 MiB transfer bandwidth {bandwidth_gb_s:.2f} GiB/s below 80% of peak"


def test_transfer_fallback_and_logging(available_gpus, caplog):
    """Ensure that the transfer function falls back to PCIe and logs a warning."""
    src, dst = available_gpus[0], available_gpus[1]
    stream = torch.cuda.Stream()

    # Monkey‑patch the transfer function to simulate NVLink unavailability
    original_transfer = transfer_tensor

    def mock_transfer(src: int, dst: int, tensor: Any):
        raise RuntimeError("NVLink unavailable")

    try:
        # Replace the real function with the mock
        globals()["transfer_tensor"] = mock_transfer

        with caplog.at_level(logging.WARNING, logger="axentx.surrogate"):
            # The fallback should be invoked internally; we just check that
            # the warning is logged.  The actual transfer will use PCIe.
            # For the purpose of the test, we skip the real transfer.
            try:
                transfer_tensor(src, dst, torch.randn(1, device="cuda"))
            except RuntimeError:
                # The mock raises; the real implementation should catch this
                # and fallback internally.  We simulate the fallback by
                # calling the original function.
                original_transfer(src, dst, torch.randn(1, device="cuda"))

        # Verify that a warning was logged
        warnings = [
            rec.message for rec in caplog.records if "NVLink unavailable" in rec.message
        ]
        assert warnings, "Expected a warning about NVLink unavailability to be logged"

    finally:
        # Restore the original transfer function
        globals()["transfer_tensor"] = original_transfer