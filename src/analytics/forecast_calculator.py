import numpy as np
from typing import Dict, List

class ForecastCalculator:
    def __init__(self, spending_data: List[Dict]):
        self.spending_data = spending_data

    def calculate_forecast(self) -> Dict:
        # Calculate moving averages
        moving_averages = [np.mean([x['spend'] for x in self.spending_data[i:i+7]]) for i in range(len(self.spending_data)-6)]

        # Calculate forecast
        forecast = np.mean(moving_averages)

        # Calculate confidence intervals
        ci = 1.96 * np.std(moving_averages) / np.sqrt(len(moving_averages))

        return {'forecast': forecast, 'ci': ci}

# Example usage
spending_data = [
    {'spend': 100},
    {'spend': 120},
    {'spend': 110},
    {'spend': 130},
    {'spend': 140},
    {'spend': 150},
    {'spend': 160},
    {'spend': 170},
    {'spend': 180},
    {'spend': 190},
    {'spend': 200},
    {'spend': 210},
    {'spend': 220},
    {'spend': 230},
    {'spend': 240},
    {'spend': 250},
]

calculator = ForecastCalculator(spending_data)
forecast = calculator.calculate_forecast()
print(forecast)