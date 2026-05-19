import unittest
from normalizer.encoding_detector import detect_encoding, normalize_encoding

class TestEncodingDetector(unittest.TestCase):
    def test_detect_encoding(self):
        text = "Hello, World!"
        encoding = detect_encoding(text)
        self.assertEqual(encoding, 'ascii')

    def test_normalize_encoding(self):
        text = "Hello, World!"
        encoding = detect_encoding(text)
        normalized_text = normalize_encoding(text, encoding)
        self.assertEqual(normalized_text, text)

if __name__ == '__main__':
    unittest.main()