import unittest
from surrogate_1_runner import main

class TestIntegrationExample(unittest.TestCase):
    def test_main(self):
        # Test the main function with integration
        main()

if __name__ == '__main__':
    unittest.main()