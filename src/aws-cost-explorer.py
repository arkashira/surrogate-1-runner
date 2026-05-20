import boto3
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

class AWSCostExplorer:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name='us-east-1'):
        self.client = boto3.client(
            'ce',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def get_cost_and_usage(self, time_period, granularity='MONTHLY', metrics=['UnblendedCost']):
        response = self.client.get_cost_and_usage(
            TimePeriod=time_period,
            Granularity=granularity,
            Metrics=metrics
        )
        return response

    def get_cost_forecast(self, time_period, granularity='MONTHLY', metric='UnblendedCost'):
        response = self.client.get_cost_forecast(
            TimePeriod=time_period,
            Granularity=granularity,
            Metric=metric
        )
        return response

    def generate_recommendations(self, cost_data):
        recommendations = []
        for result in cost_data['ResultsByTime']:
            for group in result['Groups']:
                if float(group['Metrics']['UnblendedCost']['Amount']) > 100:
                    recommendations.append({
                        'Service': group['Keys'][0],
                        'Cost': group['Metrics']['UnblendedCost']['Amount'],
                        'Recommendation': 'Consider optimizing or terminating unused resources.'
                    })
        return recommendations

    def analyze_cost_data(self, cost_data):
        # TO DO: implement cost analysis and actionable steps for optimization
        return cost_data

# Example usage
if __name__ == '__main__':
    aws_access_key_id = 'your_aws_access_key_id'
    aws_secret_access_key = 'your_aws_secret_access_key'
    cost_explorer = AWSCostExplorer(aws_access_key_id, aws_secret_access_key)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    time_period = {
        'Start': start_date.strftime('%Y-%m-%d'),
        'End': end_date.strftime('%Y-%m-%d')
    }

    cost_data = cost_explorer.get_cost_and_usage(time_period)
    recommendations = cost_explorer.generate_recommendations(cost_data)
    print(recommendations)