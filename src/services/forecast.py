from datetime import date, timedelta

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from statsmodels.tsa.arima.model import ARIMA

router = APIRouter()


class ForecastItem(BaseModel):
    """Single day forecast entry returned by the API."""

    date: date
    predicted_cost: float
    lower_ci: float
    upper_ci: float


def _get_historical_costs(days: int = 90) -> pd.Series:
    """
    Retrieve the last ``days`` of cost data.

    In the real system this would query a datastore; for now we synthesize
    deterministic data so the endpoint is testable without external services.
    """
    # Deterministic seed for reproducibility in tests
    rng = pd.date_range(end=pd.Timestamp.today(), periods=days)
    np.random.seed(0)
    trend = np.linspace(100, 150, days)  # simple upward trend
    noise = np.random.normal(scale=5, size=days)
    values = trend + noise
    return pd.Series(values, index=rng)


def _forecast_costs(series: pd.Series, steps: int = 30):
    """
    Fit a simple ARIMA(1,1,1) model on ``series`` and forecast ``steps`` days.
    Returns the mean forecast and the 95 % confidence interval.
    """
    model = ARIMA(series, order=(1, 1, 1))
    fitted = model.fit()
    forecast = fitted.get_forecast(steps=steps)
    mean = forecast.predicted_mean
    conf_int = forecast.conf_int(alpha=0.05)  # 95 % CI
    return mean, conf_int


@router.get("/forecast", response_model=list[ForecastItem])
def get_forecast():
    """
    Return a 30‑day cost forecast.

    The response includes a point estimate and a 95 % confidence interval for
    each day.
    """
    try:
        # 1️⃣ Gather the last 90 days of data
        historical = _get_historical_costs(days=90)

        # 2️⃣ Fit ARIMA and produce a 30‑day forecast
        mean, conf_int = _forecast_costs(historical, steps=30)

        # 3️⃣ Build the response payload
        start = date.today() + timedelta(days=1)  # forecasts start tomorrow
        result = []
        for i, (pred, (low, high)) in enumerate(zip(mean, conf_int.values)):
            result.append(
                ForecastItem(
                    date=start + timedelta(days=i),
                    predicted_cost=round(float(pred), 2),
                    lower_ci=round(float(low), 2),
                    upper_ci=round(float(high), 2),
                )
            )
        return result
    except Exception as exc:  # pragma: no cover – defensive
        raise HTTPException(status_code=500, detail=str(exc))