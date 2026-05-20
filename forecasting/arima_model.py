import warnings
from typing import Tuple, Optional

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tools.sm_exceptions import ValueWarning

# Suppress harmless warnings from statsmodels during fitting
warnings.simplefilter("ignore", ValueWarning)


class ARIMAForecaster:
    """
    Simple wrapper around statsmodels' ARIMA model to generate
    30‑day cost forecasts with configurable confidence intervals.
    """

    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1)):
        """
        Parameters
        ----------
        order: tuple
            The (p, d, q) order of the ARIMA model.
        """
        self.order = order
        self.model: Optional[ARIMA] = None
        self.results: Optional[object] = None

    def fit(self, series: pd.Series) -> None:
        """
        Fit the ARIMA model to a historical cost series.

        Parameters
        ----------
        series: pd.Series
            Historical cost data indexed by datetime.
        """
        if not isinstance(series, pd.Series):
            raise TypeError("series must be a pandas Series")
        if series.empty:
            raise ValueError("series must contain at least one observation")

        # Ensure the index is a DatetimeIndex for proper time‑series handling
        if not isinstance(series.index, pd.DatetimeIndex):
            series = series.copy()
            series.index = pd.to_datetime(series.index)

        # Fit the model; enforce stationarity/differencing handling internally
        self.model = ARIMA(series, order=self.order)
        self.results = self.model.fit()

    def forecast(
        self,
        steps: int = 30,
        alpha: float = 0.05,
    ) -> dict:
        """
        Produce a forecast for the next ``steps`` periods.

        Parameters
        ----------
        steps: int
            Number of future periods to forecast (default 30 days).
        alpha: float
            Significance level for confidence intervals (default 0.05 → 95% CI).

        Returns
        -------
        dict with keys:
            - "forecast": np.ndarray of point forecasts
            - "conf_int": np.ndarray of shape (steps, 2) with lower/upper bounds
        """
        if self.results is None:
            raise RuntimeError("Model has not been fitted. Call `fit` first.")

        forecast_res = self.results.get_forecast(steps=steps)
        mean = forecast_res.predicted_mean.values
        conf_int = forecast_res.conf_int(alpha=alpha).values  # lower, upper

        return {"forecast": mean, "conf_int": conf_int}

    def update(self, new_series: pd.Series) -> None:
        """
        Re‑fit the model with an updated series (e.g., after new data arrives).

        Parameters
        ----------
        new_series: pd.Series
            Updated historical cost series.
        """
        self.fit(new_series)