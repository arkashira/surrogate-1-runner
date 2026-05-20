import unittest
from src.compliance import compliance_dashboard, filter_and_sort_actions
from src.external_actions import get_external_actions

class TestComplianceDashboard(unittest.TestCase):
    def setUp(self):
        self.app = compliance_bp.test_client()
        self.app.testing = True

    def test_compliance_dashboard(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_filter_and_sort_actions(self):
        actions = [
            {'sha': 'abc123', 'status': 'completed'},
            {'sha': 'def456', 'status': 'pending'}
        ]
        query_params = {'status': 'completed'}
        filtered_sorted = filter_and_sort_actions(actions, query_params)
        self.assertEqual(len(filtered_sorted), 1)
        self.assertEqual(filtered_sorted[0]['sha'], 'abc123')

if __name__ == '__main__':
    unittest.main()