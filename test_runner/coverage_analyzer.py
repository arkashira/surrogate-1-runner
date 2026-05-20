import os
import time
from typing import Dict, List

class CoverageImpactScorer:
    def __init__(self, test_results: List[Dict]):
        self.test_results = test_results

    def calculate_coverage_impact(self) -> List[Dict]:
        scored_results = []
        for result in self.test_results:
            coverage_impact = self._calculate_coverage_impact(result)
            result['coverage_impact'] = coverage_impact
            scored_results.append(result)
        return scored_results

    def _calculate_coverage_impact(self, test_result: Dict) -> str:
        # Simple scoring for demonstration purposes
        if test_result['coverage'] > 0.8:
            return 'high'
        elif test_result['coverage'] > 0.5:
            return 'medium'
        else:
            return 'low'

    def sort_by_coverage_impact(self) -> List[Dict]:
        scored_results = self.calculate_coverage_impact()
        return sorted(scored_results, key=lambda x: ('low', 'medium', 'high').index(x['coverage_impact']))

def main():
    # Example usage
    test_results = [
        {'test_name': 'test1', 'coverage': 0.9},
        {'test_name': 'test2', 'coverage': 0.6},
        {'test_name': 'test3', 'coverage': 0.4}
    ]
    scorer = CoverageImpactScorer(test_results)
    sorted_results = scorer.sort_by_coverage_impact()
    print(sorted_results)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Response time: {time.time() - start_time} seconds")