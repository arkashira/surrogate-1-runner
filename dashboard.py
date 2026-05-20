import pandas as pd
from cost_optimization import CostOptimization

class Dashboard:
    def __init__(self, data):
        self.data = data
        self.cost_optimization = CostOptimization(data)

    def display_recommendations(self):
        recommendations = self.cost_optimization.update_recommendations()
        for recommendation in recommendations:
            print(f"Resource ID: {recommendation['resource_id']}")
            print(f"Recommendation: {recommendation['recommendation']}")
            print(f"Priority: {recommendation['priority']}")
            print()

# Example usage
if __name__ == '__main__':
    data = pd.DataFrame({
        'resource_id': [1, 2, 3],
        'cost': [1500, 600, 300]
    })
    dashboard = Dashboard(data)
    dashboard.display_recommendations()