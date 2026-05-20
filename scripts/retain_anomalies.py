import os
import time
from datetime import datetime, timedelta

def delete_old_anomalies(directory, retention_days=90):
    cutoff_time = time.time() - (retention_days * 86400)  # 86400 seconds in a day
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < cutoff_time:
                os.remove(file_path)
                print(f"Deleted {file_path}")

if __name__ == "__main__":
    anomalies_directory = '/data/anomalies'
    delete_old_anomalies(anomalies_directory)