
import boto3
import datetime
import json
from botocore.exceptions import ClientError

def get_cost_and_usage(start_date, end_date):
    client = boto3.client('cost-explorer')
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=[
                'BlendedCost'
            ],
            Filter={
                'Dimension': [
                    {
                        'Name': 'LINK_ID',
                        'Values': ['your-link-id']
                    }
                ]
            }
        )
        return response['ResultsByTime']['Results']
    except ClientError as error:
        print(error)
        return []

def detect_anomalies(data):
    threshold = 20  # Adjust this value based on your cost history
    anomalies = []
    previous_cost = None

    for item in data:
        cost = float(item['BlendedCost']['Amount'])
        timestamp = item['TimePeriod']['Start']

        if previous_cost is not None and abs(cost - previous_cost) > threshold:
            anomalies.append({
                'timestamp': timestamp,
                'cost': cost
            })

        previous_cost = cost

    return anomalies

def send_alert(anomalies):
    # Implement the logic to send alerts using a service like SNS, Slack, etc.
    pass

def main():
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()

    data = get_cost_and_usage(start_date, end_date)
    anomalies = detect_anomalies(data)

    if anomalies:
        send_alert(anomalies)

if __name__ == "__main__":
    main()