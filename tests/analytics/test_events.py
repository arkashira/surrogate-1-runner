import unittest
from src.analytics.events import record_build_completed_event

class TestAnalyticsEvents(unittest.TestCase):
    def test_record_build_completed_event(self):
        build_data = {'components': ['CPU', 'GPU'], 'total_cost': 1500}
        record_build_completed_event(build_data)
        # This test assumes the print statement in send_analytics_event is used for verification
        # In a real scenario, we'd mock the send_analytics_event function and check its call

if __name__ == '__main__':
    unittest.main()