import os
import json
import requests
from datetime import datetime, timedelta

GCP_BILLING_URL = "https://billing.reports.gcp.google.com/v1/exports"
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_CREDENTIALS_FILE = os.environ.get("GCP_CREDENTIALS_FILE")

def get_gcp_cost_data(start_date, end_date):
    if not GCP_PROJECT_ID or not GCP_CREDENTIALS_FILE:
        return {"error": "Missing GCP credentials"}

    headers = {
        "Authorization": f"Bearer {json.load(open(GCP_CREDENTIALS_FILE))['access_token']}",
        "Content-Type": "application/json",
    }

    params = {
        "projectId": GCP_PROJECT_ID,
        "startTime": start_date.isoformat(),
        "endTime": end_date.isoformat(),
    }

    response = requests.get(GCP_BILLING_URL, headers=headers, params=params)

    if response.status_code != 200:
        return {"error": f"Failed to fetch GCP cost data: {response.text}"}

    return response.json()

def fetch_gcp_cost_data(days=30):
    today = datetime.now()
    start_date = today - timedelta(days=days)
    end_date = today

    data = get_gcp_cost_data(start_date, end_date)

    if "error" in data:
        print(f"Error fetching GCP cost data: {data['error']}")
        return

    with open(f"/data/costs/{today.year}/{today.month}/{today.day}.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    fetch_gcp_cost_data()