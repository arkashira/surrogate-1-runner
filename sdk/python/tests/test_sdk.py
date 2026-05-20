import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Import the SDK module relative to this test file
from sdk import PipelineClient, PipelineError


class TestPipelineClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/api"
        self.client = PipelineClient(base_url=self.base_url)

    @patch("sdk.requests.Session.post")
    def test_start_pipeline_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {"job_id": "12345"}
        mock_post.return_value = mock_resp

        payload = {"input": "s3://bucket/file.txt"}
        job_id = self.client.start_pipeline(payload)

        mock_post.assert_called_once_with(
            f"{self.base_url}/jobs",
            data=json.dumps(payload),
            timeout=10.0,
        )
        self.assertEqual(job_id, "12345")

    @patch("sdk.requests.Session.post")
    def test_start_pipeline_missing_job_id(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {}
        mock_post.return_value = mock_resp

        with self.assertRaises(PipelineError) as ctx:
            self.client.start_pipeline({"input": "x"})
        self.assertIn("missing 'job_id'", str(ctx.exception))

    @patch("sdk.requests.Session.get")
    def test_get_status_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {"status": "running"}
        mock_get.return_value = mock_resp

        status = self.client.get_status("12345")
        mock_get.assert_called_once_with(f"{self.base_url}/jobs/12345", timeout=10.0)
        self.assertEqual(status, {"status": "running"})

    @patch("sdk.requests.Session.get")
    def test_get_status_http_error(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError("404")
        mock_get.return_value = mock_resp

        with self.assertRaises(PipelineError) as ctx:
            self.client.get_status("nonexistent")
        self.assertIn("Failed to get status", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()