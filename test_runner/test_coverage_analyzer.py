import unittest
from coverage_analyzer import CoverageImpactScorer

class TestCoverageImpactScorer(unittest.TestCase):
    def test_calculate_coverage_impact(self):
        test_results = [
            {'test_name': 'test1', 'coverage': 0.9},
            {'test_name': 'test2', 'coverage': 0.6},
            {'test_name': 'test3', 'coverage': 0.4}
        ]
        scorer = CoverageImpactScorer(test_results)
        scored_results = scorer.calculate_coverage_impact()
        self.assertEqual(scored_results[0]['coverage_impact'], 'high')
        self.assertEqual(scored_results[1]['coverage_impact'], 'medium')
        self.assertEqual(scored_results[2]['coverage_impact'], 'low')

    def test_sort_by_coverage_impact(self):
        test_results = [
            {'test_name': 'test1', 'coverage': 0.9},
            {'test_name': 'test2', 'coverage': 0.6},
            {'test_name': 'test3', 'coverage': 0.4}
        ]
        scorer = CoverageImpactScorer(test_results)
        sorted_results = scorer.sort_by_coverage_impact()
        self.assertEqual(sorted_results[0]['test_name'], 'test3')
        self.assertEqual(sorted_results[1]['test_name'], 'test2')
        self.assertEqual(sorted_results[2]['test_name'], 'test1')

if __name__ == '__main__':
    unittest.main()