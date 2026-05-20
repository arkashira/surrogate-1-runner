import unittest
from unittest.mock import patch, MagicMock
from battery_guard.cli import recommend
from battery_guard.recommendations import get_recommendations

class TestRecommendations(unittest.TestCase):
    @patch('battery_guard.recommendations.get_current_metrics')
    @patch('battery_guard.recommendations.get_historical_trends')
    def test_recommendations(self, mock_get_historical_trends, mock_get_current_metrics):
        # Mock metrics and trends
        mock_get_current_metrics.return_value = {'usage_rate': 250, 'temperature': 45}
        mock_get_historical_trends.return_value = {'usage_rate_trend': 'increasing', 'temperature_trend': 'stable'}
        
        # Test recommendations
        recommendations = get_recommendations()
        self.assertGreaterEqual(len(recommendations), 1)
        self.assertLessEqual(len(recommendations), 3)
        for recommendation in recommendations:
            self.assertIn('rationale', recommendation)
            self.assertIn('command', recommendation)

    def test_cli_recommend(self):
        # Test CLI command
        runner = CliRunner()
        result = runner.invoke(recommend)
        self.assertEqual(result.exit_code, 0)
        self.assertGreater(len(result.output), 0)

if __name__ == '__main__':
    unittest.main()