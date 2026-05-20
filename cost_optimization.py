import pandas as pd
from datetime import datetime, timedelta

class CostOptimization:
    def __init__(self, data):
        self.data = data
        self.expert_recommendations = [
            "Recommendation 1: Optimize database queries",
            "Recommendation 2: Implement caching for frequently accessed data",
            "Recommendation 3: Scale down non-production environments during off-hours",
            "Recommendation 4: Use spot instances for fault-tolerant workloads",
            "Recommendation 5: Review and remove unused resources"
        ]

    def analyze_costs(self):
        # Analyze the cost data and generate data-driven recommendations
        recommendations = []
        for index, row in self.data.iterrows():
            if row['cost'] > 1000:
                recommendations.append({
                    'resource_id': row['resource_id'],
                    'recommendation': 'Consider terminating this resource as it is costing more than $1000',
                    'priority': 'high'
                })
            elif row['cost'] > 500:
                recommendations.append({
                    'resource_id': row['resource_id'],
                    'recommendation': 'Consider optimizing this resource as it is costing more than $500',
                    'priority': 'medium'
                })
            else:
                recommendations.append({
                    'resource_id': row['resource_id'],
                    'recommendation': 'This resource is within the expected cost range',
                    'priority': 'low'
                })
        return recommendations

    def generate_recommendations(self):
        # Combine data-driven and expert-based recommendations
        data_driven_recommendations = self.analyze_costs()
        recommendations = data_driven_recommendations + self.expert_recommendations
        return recommendations

    def update_recommendations(self):
        # Update the recommendations at least every 24 hours
        last_updated = datetime.now() - timedelta(days=1)
        if datetime.now() - last_updated > timedelta(days=1):
            self.recommendations = self.generate_recommendations()
            last_updated = datetime.now()
        return self.recommendations