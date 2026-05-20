
import boto3
import pandas as pd
from datetime import datetime, timedelta

class CostHistory:
    def __init__(self, aws_access_key, aws_secret_key, region):
        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)
        self.bucket = 'axentx-cost-history'
        self.prefix = 'cost_history/'

    def fetch_cost_data(self, start_date, end_date):
        date_range = pd.date_range(start=start_date, end=end_date)
        cost_data = []

        for date in date_range:
            key = f"{self.prefix}{date.strftime('%Y-%m-%d')}.csv"
            obj = self.s3.get_object(Bucket=self.bucket, Key=key)
            df = pd.read_csv(obj['Body'])
            cost_data.append(df)

        return pd.concat(cost_data)

    def save_cost_data(self, cost_data, date):
        key = f"{self.prefix}{date.strftime('%Y-%m-%d')}.csv"
        cost_data.to_csv(key, index=False)
        self.s3.upload_file(key, self.bucket)