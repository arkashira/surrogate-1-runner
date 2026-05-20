import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pathlib import Path


class CostForecastModel:
    """
    Forecast hourly cost data using Holt–Winters exponential smoothing.
    The model is trained on the last 90 days of hourly data.
    """

    def __init__(self, data_path: str | Path):
        self.data_path = Path(data_path)
        self.model = None
        self.forecast_df = None
        self.mape = None

    # ------------------------------------------------------------------
    #  Data loading / cleaning
    # ------------------------------------------------------------------
    def _load_data(self) -> pd.Series:
        """Return a DatetimeIndex‑Series of hourly costs."""
        df = pd.read_csv(self.data_path, parse_dates=['timestamp'])
        df.set_index('timestamp', inplace=True)
        # Keep only the last 90 days
        end = datetime.utcnow()
        start = end - timedelta(days=90)
        df = df.loc[start:end]
        # Ensure hourly frequency; forward‑fill missing hours
        df = df.resample('H').sum()
        df.ffill(inplace=True)
        return df['cost']

    # ------------------------------------------------------------------
    #  Model training
    # ------------------------------------------------------------------
    def train(self) -> None:
        """Fit the Holt–Winters model."""
        data = self._load_data()
        self.model = ExponentialSmoothing(
            data,
            trend='add',
            seasonal='add',
            seasonal_periods=24,          # 24‑hour seasonality
        ).fit(optimized=True)

    # ------------------------------------------------------------------
    #  Forecasting
    # ------------------------------------------------------------------
    def forecast(self, days: int = 30) -> pd.DataFrame:
        """
        Return a DataFrame with daily projected cost, lower/upper CI and MAPE.
        """
        if self.model is None:
            raise RuntimeError("Model not trained – call `train()` first.")

        steps = days * 24
        pred = self.model.forecast(steps=steps)
        ci = self.model.get_forecast(steps=steps).conf_int(alpha=0.05)  # 95% CI

        # Aggregate to daily sums
        pred_daily = pred.resample('D').sum()
        ci_daily = ci.resample('D').sum()

        df = pd.DataFrame(
            {
                'date': pred_daily.index.date,
                'projected_cost': pred_daily.values,
                'confidence_lower': ci_daily.iloc[:, 0].values,
                'confidence_upper': ci_daily.iloc[:, 1].values,
            }
        )
        df['date'] = df['date'].astype(str)

        # Store for later use
        self.forecast_df = df
        return df

    # ------------------------------------------------------------------
    #  Accuracy evaluation (MAPE)
    # ------------------------------------------------------------------
    def evaluate(self) -> float:
        """
        Back‑test on the last 90 days.
        Returns the MAPE of the last 90 days vs. the model’s 90‑day forecast.
        """
        if self.model is None:
            raise RuntimeError("Model not trained – call `train()` first.")

        # Forecast the same period that we have data for
        data = self._load_data()
        steps = len(data)
        forecast = self.model.forecast(steps=steps)

        # MAPE
        mape = np.mean(np.abs((data.values - forecast.values) / data.values)) * 100
        self.mape = mape
        return mape

    # ------------------------------------------------------------------
    #  Persist / load forecast
    # ------------------------------------------------------------------
    def to_json(self, path: str | Path) -> None:
        """Write the forecast DataFrame to JSON."""
        if self.forecast_df is None:
            raise RuntimeError("No forecast to write – call `forecast()` first.")
        self.forecast_df.to_json(path, orient="records", date_format="iso")

    @classmethod
    def from_json(cls, path: str | Path) -> pd.DataFrame:
        """Load a previously written forecast."""
        return pd.read_json(path, orient="records")