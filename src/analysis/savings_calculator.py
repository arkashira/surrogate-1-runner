import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class SavingsCalculator:
    def __init__(self, cost_data):
        self.cost_data = cost_data

    def calculate_savings(self):
        # Split data into training and testing sets
        X = self.cost_data[['usage']]
        y = self.cost_data['cost']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and fit linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predict costs based on usage
        predicted_costs = model.predict(X_test)

        # Calculate savings
        savings = (y_test - predicted_costs).sum()

        return savings

    def project_savings(self, usage_reduction):
        # Calculate projected savings based on usage reduction
        projected_savings = self.calculate_savings() * (1 - usage_reduction)

        return projected_savings