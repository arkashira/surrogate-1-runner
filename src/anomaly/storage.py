import os
import json
import uuid
from datetime import datetime, timedelta

ANOMALY_DIR = '/data/anomalies'

def save_anomaly(detection_rule_version, anomaly_data):
    """Saves the detected anomaly to a JSON file with a unique UUID."""
    anomaly_id = str(uuid.uuid4())
    anomaly_record = {
        'id': anomaly_id,
        'version': detection_rule_version,
        'data': anomaly_data,
        'timestamp': datetime.now().isoformat()
    }
    
    # Create directory structure based on current date
    now = datetime.now()
    dir_path = os.path.join(ANOMALY_DIR, str(now.year), str(now.month).zfill(2), str(now.day).zfill(2))
    os.makedirs(dir_path, exist_ok=True)
    
    # Save anomaly to JSON file
    file_path = os.path.join(dir_path, f"{anomaly_id}.json")
    with open(file_path, 'w') as f:
        json.dump(anomaly_record, f)

def delete_old_anomalies():
    """Deletes anomaly files older than 90 days."""
    cutoff_date = datetime.now() - timedelta(days=90)
    cutoff_timestamp = cutoff_date.timestamp()

    for root, dirs, files in os.walk(ANOMALY_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < cutoff_timestamp:
                os.remove(file_path)

# Unit tests
import unittest
from unittest.mock import patch, mock_open

class TestAnomalyStorage(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_save_anomaly(self, mock_makedirs, mock_open):
        save_anomaly("1.0", {"key": "value"})
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once()
    
    @patch("os.walk")
    @patch("os.path.getmtime")
    @patch("os.remove")
    def test_delete_old_anomalies(self, mock_remove, mock_getmtime, mock_walk):
        mock_walk.return_value = [('/data/anomalies', [], ['old_anomaly.json'])]
        mock_getmtime.return_value = (datetime.now() - timedelta(days=91)).timestamp()
        delete_old_anomalies()
        mock_remove.assert_called_once_with('/data/anomalies/old_anomaly.json')

if __name__ == "__main__":
    unittest.main()