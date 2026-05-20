class Reporter:
    def __init__(self):
        self.details = {}
        self.summary = ""

    def run_checks(self):
        # Implement actual checks here
        self.details = {
            'check1': 'passed',
            'check2': 'passed'
        }
        self.summary = "All checks passed"

    def add_detail(self, key: str, value: Any):
        self.details[key] = value

    def set_summary(self, summary: str):
        self.summary = summary