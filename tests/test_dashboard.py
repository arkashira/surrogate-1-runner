import unittest
from src.dashboard.dashboard import app

class TestDashboard(unittest.TestCase):
    def test_layout(self):
        html_layout = app.layout.to_dict()
        self.assertIn('H1', html_layout)

if __name__ == '__main__':
    unittest.main()