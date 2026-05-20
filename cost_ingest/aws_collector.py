import boto3
import time
from datetime import datetime, timedelta
from psycopg2 import connect, OperationalError
from psycopg2.extras import execute_values
from . import config

class AWSCostCollector:
    def __init__(self, config):
        self.config = config
        self.client = boto3.client('ce', region_name=self.config['aws_region'])
        self.db_conn = None

    def connect_db(self):
        try:
            self.db_conn = connect(
                dbname=self.config['db_name'],
                user=self.config['db_user'],
                password=self.config['db_password'],
                host=self.config['db_host'],
                port=self.config['db_port']
            )
        except OperationalError as e:
            print(f"Database connection failed due to {e}")

    def collect_cost_data(self):
        end = datetime.utcnow()
        start = end - timedelta(hours=1)

        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start.strftime('%Y-%m-%d'),
                'End': end.strftime('%Y-%m-%d')
            },
            Granularity='HOURLY',
            Metrics=['UnblendedCost'],
            Filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': ['AmazonEC2', 'AmazonS3']
                }
            }
        )

        return response['ResultsByTime']

    def handle_throttling(self, func, *args, **kwargs):
        max_retries = 5
        retry_delay = 2
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if 'ThrottlingException' in str(e):
                    time.sleep(retry_delay * (2 ** i))
                else:
                    raise e
        raise Exception("Max retries exceeded")

    def save_to_db(self, data):
        if not self.db_conn:
            self.connect_db()

        with self.db_conn.cursor() as cursor:
            query = """
                INSERT INTO cloud_costs (provider, service, amount, timestamp)
                VALUES %s
            """
            values = [
                ('AWS', item['Groups'][0]['Keys'][0], float(item['Total']['UnblendedCost']['Amount']), item['TimePeriod']['Start'])
                for item in data
            ]
            execute_values(cursor, query, values)
            self.db_conn.commit()

    def run(self):
        if not self.config['enable_aws_collector']:
            print("AWS Cost Collector is disabled.")
            return

        data = self.handle_throttling(self.collect_cost_data)
        self.save_to_db(data)


def main():
    aws_config = config.load_config()
    collector = AWSCostCollector(aws_config)
    collector.run()


if __name__ == "__main__":
    main()