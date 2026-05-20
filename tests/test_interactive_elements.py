import unittest
from src.onboarding.interactive_elements import InteractiveTourElement

class TestInteractiveTourElement(unittest.TestCase):
    def setUp(self):
        self.tour_steps = [
            {"instruction": "Step 1", "example": "Example 1"},
            {"instruction": "Step 2", "example": "Example 2"},
            {"instruction": "Step 3", "example": "Example 3"}
        ]
        self.tour = InteractiveTourElement("Test Tour", "Description", self.tour_steps)

    def test_start_tour(self):
        self.tour.start_tour()
        self.assertEqual(self.tour.current_step, 0)

    def test_next_step(self):
        self.tour.start_tour()
        self.tour.next_step()
        self.assertEqual(self.tour.current_step, 1)

    def test_prev_step(self):
        self.tour.start_tour()
        self.tour.next_step()
        self.tour.prev_step()
        self.assertEqual(self.tour.current_step, 0)

    def test_skip_tour(self):
        self.tour.skip_tour()
        self.assertEqual(self.tour.current_step, len(self.tour_steps))

    def test_retry_tour(self):
        self.tour.skip_tour()
        self.tour.retry_tour()
        self.assertEqual(self.tour.current_step, 0)


if __name__ == '__main__':
    unittest.main()