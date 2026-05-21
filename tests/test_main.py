import unittest
from unittest.mock import patch, MagicMock
from src.main import main

class TestMain(unittest.TestCase):
    @patch('src.main.ExpertInsights')
    @patch('builtins.print')
    def test_main(self, mock_print, mock_expert_insights):
        mock_insights_instance = MagicMock()
        mock_insights_instance.get_insights.return_value = {"insights": "test_insights"}
        mock_insights_instance.get_recommendations.return_value = {"recommendations": "test_recommendations"}
        mock_expert_insights.return_value = mock_insights_instance

        main()

        mock_print.assert_any_call("Expert Insights:", {"insights": "test_insights"})
        mock_print.assert_any_call("Expert Recommendations:", {"recommendations": "test_recommendations"})

if __name__ == '__main__':
    unittest.main()