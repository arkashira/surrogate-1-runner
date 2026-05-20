import unittest
from audit_request_filtering import AuditRequestFiltering

class TestAuditRequestFiltering(unittest.TestCase):
    def setUp(self):
        self.filtering = AuditRequestFiltering()
        self.filtering.add_filter({"field": "priority", "operator": "eq", "value": "high"})

    def test_apply_filters_high_priority(self):
        audit_requests = [
            {'id': 1, 'priority': 'high'},
            {'id': 2, 'priority': 'low'},
            {'id': 3, 'priority': 'high'},
        ]
        filtered_requests = self.filtering.apply_filters(audit_requests)
        self.assertEqual(len(filtered_requests), 2)
        self.assertEqual(filtered_requests[0]['priority'], 'high')
        self.assertEqual(filtered_requests[1]['priority'], 'high')

    def test_apply_filters_no_high_priority(self):
        audit_requests = [
            {'id': 2, 'priority': 'low'},
            {'id': 4, 'priority': 'medium'},
        ]
        filtered_requests = self.filtering.apply_filters(audit_requests)
        self.assertEqual(len(filtered_requests), 0)

    def test_to_json_and_from_json(self):
        json_str = self.filtering.to_json()
        new_filtering = AuditRequestFiltering.from_json(json_str)
        self.assertEqual(new_filtering.filters, self.filtering.filters)

if __name__ == '__main__':
    unittest.main()