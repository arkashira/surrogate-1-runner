from typing import Dict

class SpendingForecast:
    def __init__(self, forecast: Dict):
        self.forecast = forecast

    def get_forecast(self) -> Dict:
        return self.forecast

# Example usage
forecast = {'forecast': 150, 'ci': 10}
model = SpendingForecast(forecast)
print(model.get_forecast())