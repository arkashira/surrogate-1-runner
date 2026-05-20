"""
Battery‑Health Predictor

Usage (CLI):
    python predictor.py <csv_file>

Usage (Library):
    from predictor import HealthPredictor, batteryguard_alert
    exit_code = batteryguard_alert([(1, 80), (2, 78), ...])
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, List, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# --------------------------------------------------------------------------- #
# Core model
# --------------------------------------------------------------------------- #
class HealthPredictor:
    """
    Trains a simple linear regression model on (day, health) data and
    predicts future health values.

    Parameters
    ----------
    data : Iterable[Tuple[int, float]] | pd.DataFrame
        Either a list/tuple of (day, health) pairs or a DataFrame with
        columns ['day', 'health'].
    """

    def __init__(self, data: Union[Iterable[Tuple[int, float]], pd.DataFrame]):
        if isinstance(data, pd.DataFrame):
            if not {"day", "health"}.issubset(data.columns):
                raise ValueError("DataFrame must contain 'day' and 'health' columns")
            self.X = data[["day"]].values
            self.y = data["health"].values
        else:
            # Assume iterable of tuples
            arr = np.array(list(data), dtype=float)
            if arr.ndim != 2 or arr.shape[1] != 2:
                raise ValueError("Iterable must contain (day, health) pairs")
            self.X = arr[:, 0].reshape(-1, 1)
            self.y = arr[:, 1]

        self.model = LinearRegression()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def train(self) -> None:
        """Fit the linear regression model."""
        self.model.fit(self.X, self.y)

    def predict(self, days_ahead: int) -> np.ndarray:
        """
        Predict health for the next `days_ahead` days.

        Returns
        -------
        np.ndarray
            Array of predicted health percentages, one per future day.
        """
        if days_ahead <= 0:
            raise ValueError("days_ahead must be positive")

        last_day = int(self.X[-1, 0])
        future_days = np.arange(last_day + 1, last_day + days_ahead + 1).reshape(-1, 1)
        return self.model.predict(future_days)

    # --------------------------------------------------------------------- #
    # Convenience helpers
    # --------------------------------------------------------------------- #
    @staticmethod
    def from_csv(path: Union[str, Path]) -> "HealthPredictor":
        """Create a HealthPredictor from a CSV file."""
        df = pd.read_csv(path)
        if not {"day", "health"}.issubset(df.columns):
            raise ValueError("CSV must contain 'day' and 'health' columns")
        return HealthPredictor(df)


# --------------------------------------------------------------------------- #
# Alert wrapper
# --------------------------------------------------------------------------- #
def batteryguard_alert(
    data: Union[Iterable[Tuple[int, float]], pd.DataFrame, str, Path],
    days_ahead: int = 30,
    threshold: float = 70.0,
) -> int:
    """
    Train a model on *data*, predict *days_ahead* future days and
    emit a warning if any predicted health falls below *threshold*.

    Parameters
    ----------
    data : Iterable[Tuple[int, float]] | pd.DataFrame | str | Path
        Input data.  If a string/Path is supplied, it is treated as a CSV file.
    days_ahead : int, default 30
        Number of future days to predict.
    threshold : float, default 70.0
        Health percentage below which a warning is issued.

    Returns
    -------
    int
        1 if a warning is issued, 0 otherwise.
    """
    # Normalise input
    if isinstance(data, (str, Path)):
        predictor = HealthPredictor.from_csv(data)
    else:
        predictor = HealthPredictor(data)

    predictor.train()
    predictions = predictor.predict(days_ahead)

    if np.any(predictions < threshold):
        print(
            f"⚠️  BatteryGuard Alert: Projected health will fall below "
            f"{threshold}% in the next {days_ahead} days."
        )
        print("Suggested actions: Review recent activity logs, check battery "
              "temperature, and consider maintenance or replacement.")
        return 1
    else:
        print(f"✅ BatteryGuard: Health is stable for the next {days_ahead} days.")
        return 0


# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predictor.py <csv_file>", file=sys.stderr)
        sys.exit(2)

    csv_path = sys.argv[1]
    exit_code = batteryguard_alert(csv_path)
    sys.exit(exit_code)