import unittest
import os
import tempfile
import pyperclip
from surrogate_1.clipboard import detect_clipboard_content
from surrogate_1.main import detect_clipboard_paste, clipboard_paste_handler

class TestClipboardDetection(unittest.TestCase):
    def setUp(self):
        self.clipboard_file = tempfile.NamedTemporaryFile(delete=False)
        self.clipboard_file.write(b"Test clipboard content")
        self.clipboard_file.close()

    def tearDown(self):
        os.unlink(self.clipboard_file.name)

    @patch('surrogate_1.clipboard.pynput')
    def test_clipboard_detection(self, mock_pynput):
        mock_pynput.Controller.get = lambda: "test data"
        detected_content = detect_clipboard_content()
        self.assertEqual(detected_content, "test data")

    def test_clipboard_detection_real(self):
        pyperclip.copy("Test clipboard content")
        result = detect_clipboard_paste()
        self.assertTrue(result)

    def test_no_clipboard_detection(self):
        pyperclip.copy("")
        result = detect_clipboard_paste()
        self.assertFalse(result)

    def test_paste_cascade_trigger(self):
        pyperclip.copy("Test")
        with self.assertLogs(level='INFO') as log:
            clipboard_paste_handler()
        self.assertIn("Paste cascade triggered", log.output[0])

if __name__ == '__main__':
    unittest.main()