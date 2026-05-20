import logging
import statistics
from typing import Dict, List, Tuple

from .utils import get_metrics, send_alert

log = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Anomaly detection logic
# --------------------------------------------------------------------------- #
def compute_statistics(values: List[float]) -> Tuple[float, float]:
    """
    Compute mean and standard deviation for a list of numeric values.
    Returns (mean, stddev). If less than 2 values, stddev is set to 0.
    """
    if not values:
        return (0.0, 0.0)
    mean = statistics.mean(values)
    stddev = statistics.stdev(values) if len(values) > 1 else 0.0
    return (mean, stddev)


def detect_anomalies(
    metrics: List[Dict[str, any]], window_size: int = 20, threshold: float = 3.0
) -> List[Dict[str, any]]:
    """
    Detect anomalies in a stream of metric samples.
    Parameters:
        metrics: list of metric dicts sorted by timestamp ascending.
        window_size: number of recent samples to consider for statistics.
        threshold: z-score threshold to flag an anomaly.
    Returns:
        List of anomaly dicts containing the original metric and computed z-score.
    """
    # Group metrics by name
    by_name: Dict[str, List[float]] = {}
    for m in metrics:
        name = m.get("name")
        value = m.get("value")
        if name is None or value is None:
            continue
        by_name.setdefault(name, []).append(value)

    anomalies: List[Dict[str, any]] = []

    for name, values in by_name.items():
        # Use sliding window over the most recent samples
        recent = values[-window_size:]
        mean, stddev = compute_statistics(recent)
        if stddev == 0:
            continue  # cannot compute z-score

        # Scan the window for anomalies
        for idx, val in enumerate(recent):
            z = (val - mean) / stddev
            if abs(z) >= threshold:
                anomaly = {
                    "name": name,
                    "value": val,
                    "timestamp": metrics[-window_size + idx]["timestamp"],
                    "z_score": z,
                }
                anomalies.append(anomaly)

    return anomalies


def process_and_alert() -> None:
    """
    Main entry point: load metrics, detect anomalies, and send alerts.
    """
    metrics = get_metrics()
    if not metrics:
        log.info("No metrics to process.")
        return

    anomalies = detect_anomalies(metrics)
    if not anomalies:
        log.info("No anomalies detected.")
        return

    log.info("Detected %d anomalies; sending alerts.", len(anomalies))
    for anomaly in anomalies:
        send_alert(anomaly)


# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    process_and_alert()