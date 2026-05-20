"""
Cost forecasting module.

The class is intentionally lightweight so it can be used both
in a FastAPI background task and in a CLI script.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression


class CostForecaster:
    """
    Train a linear regression on historical cost data and
    generate a future forecast.
    """

    def __init__(self, data_path: str, forecast_path: str | None = None):
        self.data_path = data_path
        self.forecast_path = forecast_path or os.path.join(
            os.path.dirname(data_path), "cost_forecast.csv"
        )
        self.model = LinearRegression()

    # ------------------------------------------------------------------
    # Data handling
    # ------------------------------------------------------------------
    def load_data(self) -> pd.DataFrame:
        """Load CSV into a DataFrame."""
        return pd.read_csv(self.data_path)

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse dates, sort, and set index."""
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        df.set_index("date", inplace=True)
        return df

    # ------------------------------------------------------------------
    # Model training
    # ------------------------------------------------------------------
    def train(self, df: pd.DataFrame) -> None:
        """Fit the linear model on the index (time) vs cost."""
        X = np.arange(len(df)).reshape(-1, 1)          # 0,1,2,...
        y = df["cost"].values
        self.model.fit(X, y)

    # ------------------------------------------------------------------
    # Forecasting
    # ------------------------------------------------------------------
    def forecast(self, days: int = 30) -> pd.DataFrame:
        """
        Return a DataFrame with `date` and `forecasted_cost`.

        The first forecast date is the day after the last date in the
        training data.
        """
        last_date = self._last_date()
        future_dates = [last_date + timedelta(days=i) for i in range(1, days + 1)]
        X_future = np.arange(len(future_dates)).reshape(-1, 1)
        preds = self.model.predict(X_future)
        return pd.DataFrame(
            {"date": future_dates, "forecasted_cost": preds}
        )

    def _last_date(self) -> datetime:
        """Return the last date in the CSV (used as anchor)."""
        df = self.preprocess(self.load_data())
        return df.index.max()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save_forecast(self, df: pd.DataFrame) -> None:
        df.to_csv(self.forecast_path, index=False)

    def run(self, days: int = 30) -> pd.DataFrame:
        """Convenience wrapper: train → forecast → save."""
        df = self.preprocess(self.load_data())
        self.train(df)
        forecast_df = self.forecast(days)
        self.save_forecast(forecast_df)
        return forecast_df