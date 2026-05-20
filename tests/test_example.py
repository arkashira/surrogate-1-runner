import unittest
from surrogate_1_runner import main

class TestExample(unittest.TestCase):
    def test_main(self):
        # Test the main function
        main()

if __name__ == '__main__':
    unittest.main()