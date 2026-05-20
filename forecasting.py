"""
Predictive cost forecasting module.
"""

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

from models import CostDataPoint, CostForecast

def generate_forecasts(data_points: List[CostDataPoint]) -> List[CostForecast]:
    """Generate daily forecasts using trained model."""
    # Load trained model from file
    with open('trained_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Convert data points to Pandas DataFrame
    df = pd.DataFrame([point.to_dict() for point in data_points])
    
    # Generate daily forecasts
    forecasts = []
    for i in range(len(df)):
        timestamp = df.iloc[i]['timestamp']
        amount = model.predict([[timestamp]])
        forecast = CostForecast(
            predicted_date=timestamp,
            predicted_amount=amount[0],
            confidence_interval_lower=amount[0] * 0.95,
            confidence_interval_upper=amount[0] * 1.05,
            category=df.iloc[i]['category'],
            model_version='v1'
        )
        forecasts.append(forecast)
    
    return forecasts