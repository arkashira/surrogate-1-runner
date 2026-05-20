import unittest
from onboarding.tours.pr_creation import PRCreationTour

class TestPRCreationTour(unittest.TestCase):
    def test_start_tour(self):
        tour = PRCreationTour()
        tour.start_tour()

    def test_skip_tour(self):
        tour = PRCreationTour()
        tour.skip_tour()

    def test_retry_tour(self):
        tour = PRCreationTour()
        tour.retry_tour()

if __name__ == "__main__":
    unittest.main()