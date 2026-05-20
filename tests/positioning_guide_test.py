import unittest
from src.positioning_guide import create_positioning_guide

class TestPositioningGuideCreation(unittest.TestCase):
    def test_positioning_guide_creation(self):
        create_positioning_guide()
        self.assertTrue(os.path.exists('/opt/axentx/surrogate-1/positioning/positioning_guide.md'))
        self.assertTrue(os.path.exists('/opt/axentx/surrogate-1/positioning/positioning_guide.js'))
        self.assertTrue(os.path.exists('/opt/axentx/surrogate-1/positioning/positioning_guide.css'))

if __name__ == '__main__':
    unittest.main()