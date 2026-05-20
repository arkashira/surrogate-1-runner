"""
Trend Analyzer Module
~~~~~~~~~~~~~~~~~~~~~

Provides utilities to detect cost anomalies and generate pre‑emptive alerts.

The module expects a pandas DataFrame with a DateTimeIndex and a single
numeric column named ``cost`` representing hourly cost in USD.

Functions
---------
detect_anomalies(df, window=24, threshold=1.5)
    Identify timestamps where the cost exceeds the rolling mean by
    ``threshold`` standard deviations.

generate_preemptive_alerts(df, window=24, threshold=1.5, alert_window=48)
    Return a DataFrame of alerts that are triggered 24‑48 h before a
    detected spike.  The alert contains the predicted spike time,
    the current cost, and the alert window.
"""

import pandas as pd
from typing import List, Tuple


def _rolling_stats(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Compute rolling mean and std for the cost series.
    """
    rolling_mean = df["cost"].rolling(window=window, min_periods=1).mean()
    rolling_std = df["cost"].rolling(window=window, min_periods=1).std()
    return pd.DataFrame(
        {"rolling_mean": rolling_mean, "rolling_std": rolling_std}, index=df.index
    )


def detect_anomalies(
    df: pd.DataFrame, window: int = 24, threshold: float = 1.5
) -> pd.DataFrame:
    """
    Detect cost anomalies.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with DateTimeIndex and a ``cost`` column.
    window : int
        Window size in hours for rolling statistics.
    threshold : float
        Number of standard deviations above the mean to flag an anomaly.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the timestamps of detected anomalies and
        the corresponding cost values.
    """
    if "cost" not in df.columns:
        raise ValueError("DataFrame must contain a 'cost' column")

    stats = _rolling_stats(df, window)
    anomaly_mask = df["cost"] > stats["rolling_mean"] + threshold * stats["rolling_std"]
    anomalies = df[anomaly_mask].copy()
    anomalies["anomaly"] = True
    return anomalies


def generate_preemptive_alerts(
    df: pd.DataFrame,
    window: int = 24,
    threshold: float = 1.5,
    alert_window: int = 48,
) -> pd.DataFrame:
    """
    Generate alerts that are triggered 24‑48 h before a detected spike.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with DateTimeIndex and a ``cost`` column.
    window : int
        Window size in hours for rolling statistics.
    threshold : float
        Threshold for anomaly detection.
    alert_window : int
        Number of hours before the spike to trigger an alert.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
            - ``alert_time``: when the alert is issued
            - ``spike_time``: when the spike is expected
            - ``current_cost``: cost at alert time
            - ``predicted_spike_cost``: cost at spike time
    """
    anomalies = detect_anomalies(df, window, threshold)
    alerts = []

    for spike_time in anomalies.index:
        alert_time = spike_time - pd.Timedelta(hours=alert_window)
        if alert_time in df.index:
            alerts.append(
                {
                    "alert_time": alert_time,
                    "spike_time": spike_time,
                    "current_cost": df.at[alert_time, "cost"],
                    "predicted_spike_cost": df.at[spike_time, "cost"],
                }
            )

    return pd.DataFrame(alerts).set_index("alert_time") if alerts else pd.DataFrame()


# End of trend_analyzer.py