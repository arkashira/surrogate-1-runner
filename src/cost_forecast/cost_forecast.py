from datetime import datetime, timedelta
from .prophet_wrapper import ProphetWrapper, normalize_data, get_cost_data

def generate_cost_forecast():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    cost_data = get_cost_data(start_date, end_date)
    normalized_data = normalize_data(cost_data)

    prophet_wrapper = ProphetWrapper(normalized_data)
    prophet_wrapper.train()

    mae = prophet_wrapper.backtest()
    if mae > 0.1 * normalized_data['y'].mean():
        raise ValueError("Forecast error exceeds 10% of actual spend")

    forecast = prophet_wrapper.forecast(periods=30)
    return forecast.to_dict('records')