import numpy as np
import pandas as pd
import pytest

from forecasting.arima_model import ARIMAForecaster


@pytest.fixture
def synthetic_cost_series():
    """Generate a deterministic synthetic cost series (100 days)."""
    rng = pd.date_range(start="2023-01-01", periods=100, freq="D")
    # Simple trend + seasonality + noise
    trend = np.linspace(100, 200, 100)
    season = 10 * np.sin(2 * np.pi * np.arange(100) / 30)
    noise = np.random.normal(scale=2.0, size=100)
    values = trend + season + noise
    return pd.Series(values, index=rng)


def test_arima_forecast_shape(synthetic_cost_series):
    forecaster = ARIMAForecaster(order=(2, 1, 2))
    forecaster.fit(synthetic_cost_series)

    result = forecaster.forecast(steps=30, alpha=0.05)

    # Verify output keys
    assert "forecast" in result and "conf_int" in result

    # Forecast should be length 30
    assert isinstance(result["forecast"], np.ndarray)
    assert result["forecast"].shape == (30,)

    # Confidence intervals should be (30, 2)
    assert isinstance(result["conf_int"], np.ndarray)
    assert result["conf_int"].shape == (30, 2)

    # Lower bound should be <= forecast <= upper bound
    lower, upper = result["conf_int"][:, 0], result["conf_int"][:, 1]
    assert np.all(lower <= result["forecast"])
    assert np.all(result["forecast"] <= upper)


def test_update_refits_model(synthetic_cost_series):
    forecaster = ARIMAForecaster()
    forecaster.fit(synthetic_cost_series)

    # Append new data points
    new_dates = pd.date_range(start="2023-04-11", periods=5, freq="D")
    new_values = np.linspace(210, 220, 5) + np.random.normal(scale=2.0, size=5)
    extended_series = synthetic_cost_series.append(pd.Series(new_values, index=new_dates))

    # Update model
    forecaster.update(extended_series)

    # Should still produce forecasts without error
    result = forecaster.forecast(steps=10)
    assert result["forecast"].shape == (10,)