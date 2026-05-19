"""Prediction logic for BatteryGuard."""

from datetime import datetime
from typing import List, Tuple

Metric = Tuple[datetime, float]

def predict_health(
    metrics: List[Metric], horizon_days: int = 30
) -> float:
    """
    Predict battery health after `horizon_days` using simple linear regression.

    Parameters
    ----------
    metrics : List[Metric]
        List of (timestamp, health) tuples, sorted by timestamp.
    horizon_days : int
        Number of days into the future to predict.

    Returns
    -------
    float
        Predicted health in the range [0, 100].
    """
    if len(metrics) < 2:
        # Not enough data – fall back to the most recent value
        return metrics[-1][1] if metrics else 100.0

    # Convert timestamps to days since the first sample
    xs = [(ts - metrics[0][0]).days for ts, _ in metrics]
    ys = [h for _, h in metrics]

    n = len(xs)
    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_xy = sum(x * y for x, y in zip(xs, ys))
    sum_x2 = sum(x * x for x in xs)

    denom = n * sum_x2 - sum_x * sum_x
    if denom == 0:
        return ys[-1]

    m = (n * sum_xy - sum_x * sum_y) / denom
    b = (sum_y - m * sum_x) / n

    # Predict health after `horizon_days`
    future_x = (metrics[-1][0] - metrics[0][0]).days + horizon_days
    predicted = m * future_x + b

    # Clamp to 0‑100
    return max(0.0, min(100.0, predicted))