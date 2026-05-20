import os
import json
import math
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# 轻量级备用预测方法（当statsmodels不可用时）
def _naive_forecast(series: pd.Series, steps: int) -> pd.Series:
    if series.empty:
        return pd.Series([0.0] * steps)
    last_value = series.iloc[-1] if not series.empty else 0.0
    return pd.Series([last_value] * steps, index=pd.RangeIndex(start=len(series), stop=len(series) + steps))

def _load_time_series(path: str) -> pd.Series:
    """加载历史时间序列数据"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Historical data not found at {path}")
    df = pd.read_csv(path, parse_dates=["date"])
    if "date" not in df.columns or "value" not in df.columns:
        raise ValueError("Historical data must have 'date' and 'value' columns")
    ts = df.set_index("date").asfreq("D")["value"]
    ts = ts.fillna(method="ffill")
    return ts

def _holt_winters_forecast(series: pd.Series, steps: int) -> Optional[pd.Series]:
    """使用Holt-Winters指数平滑法进行预测"""
    try:
        model = ExponentialSmoothing(
            series,
            trend="add",
            seasonal=None,
            damped_trend=True,
            seasonal_periods=7  # 默认7天季节性（可配置）
        )
        fit = model.fit(optimized=True)
        return fit.forecast(steps)
    except Exception:
        return None

def _compute_forecast(series: pd.Series, horizon_days: int, method: str = "holt_winters") -> pd.Series:
    """计算最终预测序列"""
    steps = max(1, int(horizon_days))
    if method == "holt_winters":
        forecast = _holt_winters_forecast(series, steps)
        if forecast is not None:
            return forecast
    return _naive_forecast(series, steps)

def forecast_cost_and_budget(
    historical_csv: str,
    horizon_days: Optional[int] = None,
    method: str = "holt_winters",
    seasonal_periods: int = 7
) -> Dict[str, Any]:
    """生成成本预测和预算分析结果"""
    ts = _load_time_series(historical_csv)
    horizon = horizon_days if horizon_days is not None else 30  # 默认30天
    
    forecast_series = _compute_forecast(ts, horizon, method)
    
    start_date = ts.index[-1] + timedelta(days=1) if not ts.empty else datetime.utcnow().date()
    forecast_dates = [start_date + timedelta(days=i) for i in range(len(forecast_series))]
    
    return {
        "forecast": forecast_series.to_list(),
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": forecast_dates[-1].strftime("%Y-%m-%d") if forecast_dates else "",
        "horizon_days": horizon,
        "method": method,
        "data_source": historical_csv,
        "seasonal_periods": seasonal_periods
    }

def main():
    """CLI测试入口"""
    import argparse
    parser = argparse.ArgumentParser(description="Cost forecasting tool")
    parser.add_argument("--csv", required=True, help="Historical data CSV path")
    parser.add_argument("--horizon", type=int, default=None, help="Forecast horizon in days")
    parser.add_argument("--method", default="holt_winters", help="Forecast method")
    parser.add_argument("--seasonal", type=int, default=7, help="Seasonal periods")
    args = parser.parse_args()
    
    result = forecast_cost_and_budget(
        args.csv,
        horizon_days=args.horizon,
        method=args.method,
        seasonal_periods=args.seasonal
    )
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()