class AlertSettings:
    def __init__(self, threshold_multiplier=3.0, window_size_days=30):
        self.threshold_multiplier = threshold_multiplier
        self.window_size_days = window_size_days

    def configure(self, threshold_multiplier=None, window_size_days=None):
        if threshold_multiplier is not None:
            self.threshold_multiplier = threshold_multiplier
        if window_size_days is not None:
            self.window_size_days = window_size_days

    def get_threshold_multiplier(self):
        return self.threshold_multiplier

    def get_window_size_days(self):
        return self.window_size_days


def load_alert_settings():
    # Placeholder for loading settings from a config file or environment variables
    return AlertSettings()