import unittest
from unittest.mock import patch
from .api.roth_controller import roth_guide
from .models.roth import get_roth_guide_steps

class TestRothController(unittest.TestCase):

    @patch('surrogate_1.models.roth.get_roth_guide_steps')
    def test_roth_guide(self, mock_get_roth_guide_steps):
        mock_get_roth_guide_steps.return_value = [
            {
                "title": "Step 1: Determine Eligibility",
                "description": "Check if you qualify to contribute to a Roth IRA based on your income.",
                "legal_reference": "https://www.irs.gov/publications/p590a"
            }
        ]
        response = roth_guide()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_get_roth_guide_steps.return_value)

if __name__ == '__main__':
    unittest.main()