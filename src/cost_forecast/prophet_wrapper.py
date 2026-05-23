import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from datetime import datetime, timedelta

class ProphetWrapper:
    def __init__(self, data):
        self.data = data
        self.model = Prophet()

    def train(self):
        self.model.fit(self.data)

    def forecast(self, periods=30):
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        return forecast[['ds', 'yhat']].tail(periods)

    def backtest(self, initial='180 days', period='30 days', horizon='30 days'):
        df_cv = cross_validation(self.model, initial=initial, period=period, horizon=horizon)
        df_p = performance_metrics(df_cv)
        return df_p['mae'].mean()

def normalize_data(data):
    data = data.copy()
    data['ds'] = pd.to_datetime(data['ds'])
    data['y'] = data['amount_usd']
    return data[['ds', 'y']]

def get_cost_data(start_date, end_date):
    # This function should be implemented to fetch cost data from the database
    # For the purpose of this example, we will return a dummy DataFrame
    dates = pd.date_range(start=start_date, end=end_date)
    data = pd.DataFrame({'ds': dates, 'amount_usd': [i * 100 for i in range(len(dates))]})
    return data