import unittest
from src.paste_handlers.ax_handler import AXDirectPasteHandler

class TestAXDirectPasteHandler(unittest.TestCase):
    def setUp(self):
        self.handler = AXDirectPasteHandler()

    def test_attempt_paste(self):
        self.handler.attempt_paste()
        self.assertTrue(self.handler.get_success_status(), "AX direct paste should succeed")

if __name__ == '__main__':
    unittest.main()