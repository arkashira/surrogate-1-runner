import unittest
from analytics_engine import AnalyticsEngine

class TestAnalyticsEngine(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {'converted': 1, 'clicked': 0},
            {'converted': 0, 'clicked': 1},
            {'converted': 1, 'clicked': 1},
            {'converted': 0, 'clicked': 0}
        ]
        self.test_df = pd.DataFrame(self.test_data)
        self.test_df.to_csv('test_data.csv', index=False)
        self.engine = AnalyticsEngine('test_data.csv')

    def tearDown(self):
        import os
        os.remove('test_data.csv')

    def test_track_kpis(self):
        kpis = self.engine.track_kpis()
        expected_kpis = {'conversion_rate': 0.5, 'click_through_rate': 0.5}
        self.assertEqual(kpis, expected_kpis)

    def test_generate_insights(self):
        insights = self.engine.generate_insights()
        self.assertEqual(len(insights), 2)
        self.assertIn('kpi', insights[0])
        self.assertIn('value', insights[0])
        self.assertIn('actionable_insight', insights[0])

if __name__ == '__main__':
    unittest.main()