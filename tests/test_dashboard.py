import unittest
from unittest.mock import patch
from src.dashboard import app

class TestDashboard(unittest.TestCase):
    def test_launch_session(self):
        with patch("src.dashboard.launch_session_logic") as mock_launch_session:
            response = app.callback(
                Output("session-status", "children"),
                [Input("launch-button", "n_clicks")],
                [dash.dependencies.State("instance-select", "value")],
            )
            mock_launch_session.assert_called_once()

if __name__ == "__main__":
    unittest.main()