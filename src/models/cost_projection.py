import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class CostProjectionModel:
    def __init__(self, cost_data):
        self.cost_data = cost_data

    def train_model(self):
        # Split data into training and testing sets
        X = self.cost_data[['usage']]
        y = self.cost_data['cost']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and fit random forest regressor model
        model = RandomForestRegressor()
        model.fit(X_train, y_train)

        return model

    def project_costs(self, model, usage):
        # Predict costs based on usage
        predicted_costs = model.predict(usage)

        return predicted_costs