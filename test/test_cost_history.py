
import unittest
from unittest.mock import patch
from cost_history import CostHistory
import pandas as pd

class TestCostHistory(unittest.TestCase):
    def setUp(self):
        self.aws_access_key = 'test_access_key'
        self.aws_secret_key = 'test_secret_key'
        self.region = 'us-west-2'
        self.ch = CostHistory(self.aws_access_key, self.aws_secret_key, self.region)

    @patch('cost_history.boto3.client')
    def test_fetch_cost_data(self, mock_s3):
        mock_s3.return_value.get_object.return_value = {
            'Body': pd.read_csv(StringIO('date,cost\n2022-01-01,10\n2022-01-02,20')).values
        }

        start_date = '2022-01-01'
        end_date = '2022-01-02'

        result = self.ch.fetch_cost_data(start_date, end_date)

        expected = pd.read_csv(StringIO('date,cost\n2022-01-01,10\n2022-01-02,20'))
        pd.testing.assert_frame_equal(result, expected)

## Summary
- Implemented `CostHistory` class to fetch and save cost data from AWS S3.
- Added a test case for `fetch_cost_data` method using `unittest` and `patch` for mocking AWS S3 client.
- The solution allows for historical cost data collection based on date ranges.