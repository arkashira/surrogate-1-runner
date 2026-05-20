class AuditTrail:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_latest_entry(self):
        if not self.entries:
            return None
        return self.entries[-1]

    def get_previous_entry(self):
        if len(self.entries) < 2:
            return None
        return self.entries[-2]