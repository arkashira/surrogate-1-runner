import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class ForecastService:
    def __init__(self):
        self.model = LinearRegression()
        self.train_model()

    def train_model(self):
        # Load latest cost data
        cost_data = self.load_cost_data()
        
        # Prepare features and target variable
        X = cost_data[['date']]
        y = cost_data['cost']
        
        # Train the model
        self.model.fit(X, y)

    def load_cost_data(self):
        # Placeholder function to load cost data
        # Replace with actual data loading logic
        data = {
            'date': pd.date_range(start='2023-01-01', periods=100),
            'cost': range(100)
        }
        return pd.DataFrame(data)

    def predict(self, start_date, end_date):
        # Generate date range for prediction
        dates = pd.date_range(start=start_date, end=end_date)
        X_pred = pd.DataFrame(dates, columns=['date'])
        
        # Predict costs
        predicted_costs = self.model.predict(X_pred)
        
        return dict(zip(dates, predicted_costs))

def get_forecast(start_date, end_date):
    service = ForecastService()
    return service.predict(start_date, end_date)