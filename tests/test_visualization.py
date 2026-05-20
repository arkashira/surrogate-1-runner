import unittest
from unittest.mock import patch
import matplotlib.pyplot as plt
import pandas as pd
from src.ui.visualization import DiskGeometryVisualization

class TestDiskGeometryVisualization(unittest.TestCase):
    @patch.object(plt, 'show')
    def test_display_histogram(self, mock_show):
        data = {
            'disk_size': [500, 1000, 2000, 3000]
        }
        df = pd.DataFrame(data)
        viz = DiskGeometryVisualization(df)
        viz.display_histogram()
        self.assertTrue(mock_show.called)

    @patch.object(plt, 'show')
    def test_display_pie_chart(self, mock_show):
        data = {
            'used_space': [200, 400, 800, 1200],
            'free_space': [300, 600, 1200, 1800]
        }
        df = pd.DataFrame(data)
        viz = DiskGeometryVisualization(df)
        viz.display_pie_chart()
        self.assertTrue(mock_show.called)

    @patch.object(plt, 'show')
    def test_display_line_chart(self, mock_show):
        data = {
            'timestamp': pd.date_range(start='2023-01-01', periods=4, freq='M'),
            'disk_usage': [40, 40, 40, 40]
        }
        df = pd.DataFrame(data)
        viz = DiskGeometryVisualization(df)
        viz.display_line_chart()
        self.assertTrue(mock_show.called)

if __name__ == "__main__":
    unittest.main()