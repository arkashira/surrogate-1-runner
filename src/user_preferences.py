class UserPreferences:
    def __init__(self):
        self.preferences = {
            'brightness': 1.0,
            'auto_adjust': True
        }

    def set_brightness(self, brightness):
        """Set the brightness preference."""
        self.preferences['brightness'] = brightness
        self.preferences['auto_adjust'] = False

    def get_preferences(self):
        """Get the current user preferences."""
        return self.preferences