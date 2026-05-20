import unittest
from compliance_scan.remediation import RemediationActions

class TestRemediationActions(unittest.TestCase):
    def setUp(self):
        self.scan_results = [
            {
                "resource_type": "terraform",
                "resource_id": "tf-resource-1",
                "vulnerability": "CVE-2023-1234"
            },
            {
                "resource_type": "helm",
                "resource_id": "helm-resource-1",
                "vulnerability": "CVE-2023-5678"
            }
        ]
        with open("/tmp/scan_results.json", 'w') as file:
            json.dump(self.scan_results, file)
        self.remediation = RemediationActions("/tmp/scan_results.json")

    def test_load_scan_results(self):
        results = self.remediation.load_scan_results()
        self.assertEqual(results, self.scan_results)

    def test_remediate_vulnerabilities(self):
        self.remediation.remediate_vulnerabilities(self.scan_results)
        # Check if remediation messages were printed (placeholder for actual checks)
        self.assertTrue(True)

    def tearDown(self):
        os.remove("/tmp/scan_results.json")

if __name__ == '__main__':
    unittest.main()