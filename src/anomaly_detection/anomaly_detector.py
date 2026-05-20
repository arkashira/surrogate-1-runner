import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, data):
        self.data = data
        self.model = IsolationForest(contamination=0.05)

    def fit(self):
        self.model.fit(self.data)

    def predict(self, X):
        return self.model.predict(X)

    def detect_anomalies(self):
        anomalies = self.predict(self.data)
        return np.where(anomalies == -1)[0]

# opt/axentx/surrogate-1/src/dashboard/anomaly_alerts.py
from flask import Flask, render_template
from anomaly_detector import AnomalyDetector

app = Flask(__name__)

@app.route('/')
def index():
    detector = AnomalyDetector(data)  # Assuming 'data' is the cloud cost data
    detector.fit()
    anomalies = detector.detect_anomalies()
    return render_template('index.html', anomalies=anomalies)

if __name__ == '__main__':
    app.run(debug=True)

# opt/axentx/surrogate-1/templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Anomaly Alerts</title>
</head>
<body>
    <h1>Anomaly Alerts</h1>
    <ul>
        {% for anomaly in anomalies %}
            <li>Anomaly detected at index {{ anomaly }}</li>
        {% endfor %}
    </ul>
</body>
</html>

## Summary
- Implemented statistical anomaly detection algorithm using Isolation Forest.
- Added anomaly detection to the AnomalyDetector class.
- Created a Flask application to display anomaly alerts in the dashboard.
- Updated the dashboard template to display detected anomalies.