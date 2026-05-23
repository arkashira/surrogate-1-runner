
import numpy as np
import pandas as pd

def calculate_anomaly_score(historical_data):
    mean = historical_data.mean()
    std = historical_data.std()
    z_scores = (historical_data - mean) / std
    anomaly_score = z_scores.abs().max()
    return anomaly_score

def detect_anomalies(historical_data, threshold=3):
    anomalies = historical_data[historical_data.abs() > threshold * historical_data.std()]
    return anomalies

def main():
    # Load historical cost data
    data = pd.read_csv('cost_data.csv')

    # Calculate anomaly score for each day
    scores = data['cost'].apply(calculate_anomaly_score, axis=1)

    # Detect anomalies based on a threshold
    anomalies = detect_anomalies(scores)

    # Save detected anomalies to a CSV file
    anomalies.to_csv('anomalies.csv')

    # Print a summary of the detected anomalies
    print(f"Detected {len(anomalies)} anomalies.")

if __name__ == "__main__":
    main()