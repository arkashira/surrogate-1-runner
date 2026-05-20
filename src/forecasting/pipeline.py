import pandas as pd
from sklearn.linear_model import LinearRegression
from src.data_processors.cloud_cost_processor import CloudCostProcessor

class ForecastingPipeline:
    def __init__(self, cloud_cost_processor: CloudCostProcessor):
        self.cloud_cost_processor = cloud_cost_processor
        self.model = LinearRegression()

    def fit(self, data):
        df = pd.DataFrame(data)
        X = df[['day']]
        y = df['cost']
        self.model.fit(X, y)

    def predict(self, days):
        X = pd.DataFrame({'day': days})
        return self.model.predict(X)

# opt/axentx/surrogate-1/src/data_processors/cloud_cost_processor.py
import boto3
import google.cloud.bigquery as bigquery
from azure.mgmt.costmanagement import CostManagementClient

class CloudCostProcessor:
    def __init__(self, cloud_type):
        self.cloud_type = cloud_type
        if cloud_type == 'aws':
            self.client = boto3.client('ce')
        elif cloud_type == 'gcp':
            self.client = bigquery.Client()
        elif cloud_type == 'azure':
            self.client = CostManagementClient()

    def get_cost_data(self, start_date, end_date):
        if self.cloud_type == 'aws':
            response = self.client.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity='DAILY',
                Metrics=['UnblendedCost']
            )
            data = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        elif self.cloud_type == 'gcp':
            query = f"SELECT day, SUM(cost) as cost FROM `project.dataset.cloud_costs` WHERE day BETWEEN '{start_date}' AND '{end_date}' GROUP BY day"
            data = self.client.query(query).to_dataframe()
        elif self.cloud_type == 'azure':
            data = self.client.cost_management.list_costs(start_date, end_date, 'Daily', 'UnblendedCost')
        return data

# Summary:
- Implemented `ForecastingPipeline` class with `fit` and `predict` methods.
- Implemented `CloudCostProcessor` class with `get_cost_data` method supporting AWS, GCP, and Azure.
- The pipeline fetches historical cost data, fits a linear regression model, and predicts future costs.