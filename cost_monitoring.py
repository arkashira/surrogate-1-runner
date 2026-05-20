import boto3
import requests
import json
from datetime import datetime, timedelta
import time

class CostMonitoring:
    def __init__(self, config):
        self.config = config
        self.cloudwatch = boto3.client('cloudwatch')
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(config['dynamodb_table'])
        self.alert_threshold = config['alert_threshold']
        self.alert_tools = config['alert_tools']

    def get_cost_data(self):
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[{'Name': 'Currency', 'Value': 'USD'}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,
            Statistics=['Sum']
        )
        return response['Datapoints']

    def check_for_anomalies(self, cost_data):
        if not cost_data:
            return False
        latest_cost = cost_data[0]['Sum']
        previous_cost = self.table.get_item(Key={'timestamp': str(datetime.utcnow() - timedelta(hours=2))}).get('Item', {}).get('cost', 0)
        if latest_cost > previous_cost * self.alert_threshold:
            return True
        return False

    def send_alert(self, message):
        for tool in self.alert_tools:
            if tool['name'] == 'Datadog':
                requests.post(tool['webhook_url'], json={'text': message})
            elif tool['name'] == 'Prometheus':
                requests.post(tool['webhook_url'], json={'msg': message})

    def run(self):
        while True:
            cost_data = self.get_cost_data()
            if self.check_for_anomalies(cost_data):
                message = f"Cost spike detected at {datetime.utcnow()}. Current cost: {cost_data[0]['Sum']}"
                self.send_alert(message)
            time.sleep(3600)

if __name__ == "__main__":
    config = {
        'dynamodb_table': 'CostData',
        'alert_threshold': 1.5,
        'alert_tools': [
            {'name': 'Datadog', 'webhook_url': 'https://api.datadoghq.com/api/v1/events'},
            {'name': 'Prometheus', 'webhook_url': 'http://prometheus-server/webhook'}
        ]
    }
    monitor = CostMonitoring(config)
    monitor.run()