import pytest

from monitoring.metrics import monitor_resource_usage, log_metrics


def test_monitor_resource_usage_basic():
    """Ensure the context manager returns a dict with expected keys."""
    with monitor_resource_usage() as before:
        # simple workload
        sum(i for i in range(1000000))
    metrics = before  # the yielded value is the 'before' snapshot
    # The context manager returns the metrics dict after the block
    # but the 'before' snapshot is yielded; we capture it here
    # and then call the context manager again to get the full dict.
    with monitor_resource_usage() as _:
        pass
    # The returned dict should contain all keys
    assert isinstance(metrics, dict)
    for key in ("before", "after", "delta_cpu_percent",
                "delta_memory_rss", "delta_memory_vms"):
        assert key in metrics


def test_log_metrics_captures_output(capsys):
    """log_metrics should print to stdout."""
    with monitor_resource_usage() as before:
        pass
    metrics = before
    log_metrics("test_block", metrics)
    captured = capsys.readouterr()
    assert "CPU percent before" in captured.out
    assert "CPU percent after" in captured.out
    assert "RSS delta" in captured.out