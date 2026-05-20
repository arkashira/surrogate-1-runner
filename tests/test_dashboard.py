import unittest
from unittest.mock import patch
from src.surrogate.dashboard import app

class TestDashboard(unittest.TestCase):
    def test_layout(self):
        with patch('dash.Dash.layout', return_value='test_layout'):
            self.assertEqual(app.layout, 'test_layout')

if __name__ == '__main__':
    unittest.main()