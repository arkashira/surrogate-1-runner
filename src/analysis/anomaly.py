
import pandas as pd
import numpy as np
from datetime import timedelta, datetime

def calculate_7_day_rolling_average(data, column, window=7):
    return data[column].rolling(window).mean()

def detect_anomalies(data, threshold=0.3):
    rolling_avg = calculate_7_day_rolling_average(data, 'cost')
    return data[(data['cost'] / rolling_avg) > threshold]

def send_alert(account_id, service, current_cost, previous_avg, percentage_change, slack_webhook_url):
    alert_payload = {
        'account_id': account_id,
        'service': service,
        'current_cost': current_cost,
        'previous_avg': previous_avg,
        'percentage_change': percentage_change,
        'link_to_dashboard': 'https://example.com/dashboard'
    }
    # Replace the following line with the actual Slack webhook URL
    response = requests.post(slack_webhook_url, json=alert_payload)

def process_data():
    # Load data from the database or another source
    data = pd.read_csv('data/cost_data.csv')

    # Detect anomalies and store them in a new DataFrame
    anomalies = detect_anomalies(data)

    # Save the anomalies to a new CSV file
    anomalies.to_csv('data/alerts.csv', index=False)

    # Send alerts for detected anomalies
    for index, row in anomalies.iterrows():
        send_alert(row['account_id'], row['service'], row['cost'], row['previous_avg'], row['percentage_change'], '<slack-webhook>')

# Run the process_data function
process_data()