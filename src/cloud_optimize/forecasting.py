import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

class Forecasting:
    def __init__(self, historical_data):
        self.historical_data = historical_data

    def forecast_costs(self, days=30):
        # Convert historical data to DataFrame
        df = pd.DataFrame(self.historical_data)

        # Convert date strings to datetime objects
        df['date'] = pd.to_datetime(df['date'])

        # Sort data by date
        df.sort_values('date', inplace=True)

        # Prepare data for forecasting
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        X = df[['days_since_start']]
        y = df['cost']

        # Create a polynomial regression model
        model = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())
        model.fit(X, y)

        # Forecast costs for the next 'days' days
        future_dates = [df['date'].max() + timedelta(days=i) for i in range(1, days+1)]
        future_days_since_start = [(date - df['date'].min()).days for date in future_dates]
        future_X = pd.DataFrame({'days_since_start': future_days_since_start})
        future_costs = model.predict(future_X)

        # Create a DataFrame with the forecasted data
        forecast_df = pd.DataFrame({
            'date': future_dates,
            'cost': future_costs
        })

        return forecast_df