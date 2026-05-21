import pandas as pd
from .forecasting import Forecasting

class CloudOptimizeDashboard:
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.forecasting = Forecasting(historical_data)

    def display_forecast(self, days=30):
        forecast_df = self.forecasting.forecast_costs(days)
        print("Forecasted Cloud Costs:")
        print(forecast_df)

    def set_budget(self, budget):
        self.budget = budget

    def check_budget(self, forecast_df):
        total_cost = forecast_df['cost'].sum()
        if total_cost > self.budget:
            print(f"Alert: The forecasted cost of {total_cost} exceeds the set budget of {self.budget}.")
        else:
            print(f"The forecasted cost of {total_cost} is within the set budget of {self.budget}.")