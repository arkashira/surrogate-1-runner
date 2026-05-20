import time
import unittest
from typing import List, Dict

from src.ranker import score_builds


class TestScoringInferenceTime(unittest.TestCase):
    def setUp(self) -> None:
        # Generate a modest list of dummy builds.
        self.builds: List[Dict[str, int]] = [
            {"cpu": i, "gpu": i * 2, "ram": i * 4} for i in range(10)
        ]

    def test_inference_time_per_build_under_300ms(self) -> None:
        """
        Ensure that scoring the candidate builds averages less than 300 ms per build.
        """
        start = time.perf_counter()
        top_builds = score_builds(self.builds, top_n=3)
        elapsed = time.perf_counter() - start

        # Sanity check: we got the expected number of results.
        self.assertEqual(len(top_builds), 3)

        per_build_ms = (elapsed / len(self.builds)) * 1000  # convert to ms
        self.assertLess(
            per_build_ms,
            300,
            f"Inference took {per_build_ms:.2f} ms per build, exceeding 300 ms limit",
        )


if __name__ == "__main__":
    unittest.main()