import datetime
import requests

def fetch_last_90_days_data():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=90)
    url = f"http://your-api-url/api/v1/costs/data?start={start_date}&end={end_date}"
    response = requests.get(url)
    return response.json()

def compute_forecast(data):
    # Placeholder for Holt-Winters exponential smoothing implementation
    # This should be replaced with an actual implementation
    forecast = {
        "projected_total": sum(data) / len(data) * 30,  # Simplified projection
        "confidence_interval": [forecast["projected_total"] * 0.9, forecast["projected_total"] * 1.1]
    }
    return forecast

def update_forecast(forecast):
    url = "http://your-api-url/api/v1/costs/forecast"
    payload = {
        "forecast": forecast,
        "days": 30
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200

def main():
    data = fetch_last_90_days_data()
    forecast = compute_forecast(data)
    success = update_forecast(forecast)
    if not success:
        print("Failed to update forecast")

if __name__ == "__main__":
    main()