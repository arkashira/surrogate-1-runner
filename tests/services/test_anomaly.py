import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from services.anomaly import BaselineCalculator, DataService

class TestBaselineCalculator(unittest.TestCase):
    def setUp(self):
        self.mock_data_service = MagicMock(spec=DataService)
        self.calculator = BaselineCalculator(self.mock_data_service)

    def test_calculate_baseline(self):
        # Setup mock data
        mock_data_points = [100.0, 105.0, 110.0, 108.0, 112.0, 107.0, 115.0]
        self.mock_data_service.query_data_points.return_value = mock_data_points

        # Call method
        baseline = self.calculator.calculate_baseline("compute", "account123")

        # Assertions
        self.assertEqual(baseline, 108.0)
        self.mock_data_service.query_data_points.assert_called_once()

    def test_get_data_points(self):
        # Setup mock data
        mock_data_points = [100.0, 105.0, 110.0, 108.0, 112.0, 107.0, 115.0]
        self.mock_data_service.query_data_points.return_value = mock_data_points

        # Call method
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        data_points = self.calculator._get_data_points("compute", "account123", start_date, end_date)

        # Assertions
        self.assertEqual(data_points, mock_data_points)
        self.mock_data_service.query_data_points.assert_called_once()

if __name__ == '__main__':
    unittest.main()