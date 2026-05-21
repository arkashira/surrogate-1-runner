class AnomalyDetector:
    def __init__(self, threshold):
        self.threshold = threshold

    def detect_anomaly(self, data):
        if data > self.threshold:
            return True
        return False