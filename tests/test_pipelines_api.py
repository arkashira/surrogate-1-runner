import unittest
from unittest.mock import patch
from src.api.pipelines import api, Pipeline

class TestPipelinesAPI(unittest.TestCase):

    def setUp(self):
        self.app = api.test_client()

    @patch('src.api.pipelines.get_pipelines')
    def test_pipelines_endpoint(self, mock_get_pipelines):
        mock_pipelines = [
            Pipeline("Test Pipeline 1", datetime.now(), "Running"),
            Pipeline("Test Pipeline 2", datetime.now(), "Success"),
            Pipeline("Test Pipeline 3", datetime.now(), "Failed")
        ]
        mock_get_pipelines.return_value = mock_pipelines

        response = self.app.get('/api/pipelines')
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertIn('name', data[0])
        self.assertIn('last_run_time', data[0])
        self.assertIn('status', data[0])
        self.assertIn('status_color', data[0])

if __name__ == '__main__':
    unittest.main()