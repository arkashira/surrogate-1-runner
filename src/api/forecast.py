from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression

def fetch_historical_data():
    # Placeholder function to fetch historical cost data
    # Replace with actual data fetching logic
    return pd.DataFrame({
        'date': pd.date_range(end=datetime.now(), periods=30),
        'cost': [100 + i * 5 for i in range(30)]  # Example cost values
    })

def generate_forecast(historical_data):
    X = historical_data['date'].map(datetime.toordinal).values.reshape(-1, 1)
    y = historical_data['cost'].values

    model = LinearRegression()
    model.fit(X, y)

    future_dates = pd.date_range(start=historical_data['date'].max() + timedelta(days=1), periods=30)
    future_X = future_dates.map(datetime.toordinal).values.reshape(-1, 1)
    forecast = model.predict(future_X)

    return future_dates, forecast

def get_forecast():
    historical_data = fetch_historical_data()
    future_dates, forecast = generate_forecast(historical_data)

    labels = [date.strftime('%Y-%m-%d') for date in pd.concat([historical_data['date'], future_dates])]
    historical_costs = historical_data['cost'].tolist()
    forecasted_costs = forecast.tolist()

    return {
        'labels': labels,
        'historical': historical_costs + [None] * len(forecasted_costs),
        'forecast': [None] * len(historical_costs) + forecasted_costs
    }

if __name__ == "__main__":
    print(get_forecast())