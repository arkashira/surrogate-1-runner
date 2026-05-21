import unittest
from src.scanner.model_artifact_analyzer import ModelArtifactAnalyzer

class TestModelArtifactAnalyzer(unittest.TestCase):
    def setUp(self):
        self.model_artifacts_dir = '/tmp/model_artifacts'
        self.analyzer = ModelArtifactAnalyzer(self.model_artifacts_dir)

    def test_analyze(self):
        # Create some sample model artifact files
        with open(os.path.join(self.model_artifacts_dir, 'artifact1.json'), 'w') as f:
            json.dump({'key': 'value'}, f)

        with open(os.path.join(self.model_artifacts_dir, 'artifact2.json'), 'w') as f:
            json.dump({'key': 'value'}, f)

        # Run the analysis
        reports = self.analyzer.analyze()

        # Assert that the reports are generated correctly
        self.assertEqual(len(reports), 2)
        self.assertEqual(reports[0]['compliance_status'], 'PENDING')
        self.assertEqual(reports[1]['compliance_status'], 'PENDING')

if __name__ == '__main__':
    unittest.main()