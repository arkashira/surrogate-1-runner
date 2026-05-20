"""
Anomaly detection for cost‑pattern data.

Uses an IsolationForest trained on a rolling window of recent data.
The detector exposes a simple API:
    * train(df)
    * predict(df) -> array of -1 (anomaly) / 1 (normal)
    * detect_anomalies(df) -> DataFrame of anomalies
"""

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Optional, Dict, Any

class AnomalyDetector:
    def __init__(
        self,
        contamination: float = 0.01,
        window_size: int = 30,
        random_state: Optional[int] = 42,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Parameters
        ----------
        contamination : float
            Proportion of outliers in the data set.
        window_size : int
            Number of recent rows to keep for training.
        random_state : int | None
            Seed for reproducibility.
        config : dict | None
            Optional dict to override defaults (e.g. thresholds).
        """
        self.contamination = contamination
        self.window_size = window_size
        self.random_state = random_state
        self.config = config or {}
        self.model: Optional[IsolationForest] = None
        self.scaler = StandardScaler()
        self._history: pd.DataFrame = pd.DataFrame()

    # ------------------------------------------------------------------ #
    #  Core training / prediction
    # ------------------------------------------------------------------ #
    def _fit(self, df: pd.DataFrame) -> None:
        """Fit the IsolationForest on the current history."""
        scaled = self.scaler.fit_transform(df)
        self.model = IsolationForest(
            n_estimators=100,
            contamination=self.contamination,
            random_state=self.random_state,
            behaviour="new",  # for sklearn <1.2
        )
        self.model.fit(scaled)

    def train(self, df: pd.DataFrame) -> None:
        """Add new data to the rolling window and retrain."""
        # Keep only the last `window_size` rows
        self._history = pd.concat([self._history, df]).tail(self.window_size)
        self._fit(self._history)

    def predict(self, df: pd.DataFrame) -> pd.Series:
        """Return -1 for anomalies, 1 for normal."""
        if self.model is None:
            raise RuntimeError("Model has not been trained yet.")
        scaled = self.scaler.transform(df)
        preds = self.model.predict(scaled)
        return pd.Series(preds, index=df.index)

    # ------------------------------------------------------------------ #
    #  Convenience helpers
    # ------------------------------------------------------------------ #
    def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return the subset of `df` that were flagged as anomalies."""
        preds = self.predict(df)
        return df[preds == -1]

    # ------------------------------------------------------------------ #
    #  Export / import (optional)
    # ------------------------------------------------------------------ #
    def to_dict(self) -> Dict[str, Any]:
        """Export model parameters for persistence."""
        return {
            "contamination": self.contamination,
            "window_size": self.window_size,
            "random_state": self.random_state,
            "config": self.config,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnomalyDetector":
        """Recreate a detector from a dict."""
        return cls(
            contamination=data.get("contamination", 0.01),
            window_size=data.get("window_size", 30),
            random_state=data.get("random_state", 42),
            config=data.get("config"),
        )