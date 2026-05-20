"""
Model training module for predictive cost forecasting.
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from models import CostDataPoint, CostForecast

def train_model(data_points: List[CostDataPoint]) -> None:
    """Train model using historical cost data."""
    # Convert data points to NumPy arrays
    X = np.array([point.timestamp.timestamp() for point in data_points]).reshape(-1, 1)
    y = np.array([point.amount for point in data_points])
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train random forest regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model performance
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Model MSE: {mse:.2f}')
    
    # Save trained model to file
    import pickle
    with open('trained_model.pkl', 'wb') as f:
        pickle.dump(model, f)