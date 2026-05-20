
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class ForecastModel:
    """
    Wrapper around Holt-Winters exponential smoothing for cost forecasting.
    """
    def __init__(self, usage_series: pd.Series, freq: str = "H"):
        if not isinstance(usage_series, pd.Series):
            raise TypeError("usage_series must be a pandas Series")
        if usage_series.empty:
            raise ValueError("usage_series cannot be empty")
        self.usage = usage_series.asfreq(freq, method="ffill")
        self.freq = freq
        self.model = None
        self.residual_std = None

    def fit(self):
        seasonal_periods = 24 * 7
        self.model = ExponentialSmoothing(
            self.usage,
            trend="add",
            seasonal="add",
            seasonal_periods=seasonal_periods,
            damped_trend=False,
        ).fit(optimized=True)

        fitted_vals = self.model.fittedvalues
        residuals = self.usage - fitted_vals
        self.residual_std = np.std(residuals, ddof=1)

    def forecast(self, days: int) -> pd.DataFrame:
        self._ensure_fitted()
        forecast = self.model.forecast(steps=days * 24)
        index = pd.date_range(start=self.usage.index[-1], periods=days * 24 + 1, freq=self.freq)[1:]
        forecast_df = pd.DataFrame({
            'forecast': forecast,
            'lower_ci': forecast - 1.96 * self.residual_std,
            'upper_ci': forecast + 1.96 * self.residual_std
        }, index=index)
        return forecast_df

    def _ensure_fitted(self):
        if self.model is None or self.residual_std is None:
            raise RuntimeError("Model must be fitted before forecasting")