import unittest
from src.error_classifier import ErrorClassifier

class TestErrorClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = ErrorClassifier()

    def test_classify_timeout_error(self):
        error = "Request timed out"
        result = self.classifier.classify_error(error)
        self.assertEqual(result, "timeout")

    def test_classify_connection_error(self):
        error = "Network connection failed"
        result = self.classifier.classify_error(error)
        self.assertEqual(result, "connection")

    def test_classify_authentication_error(self):
        error = "Authentication failed"
        result = self.classifier.classify_error(error)
        self.assertEqual(result, "authentication")

    def test_classify_validation_error(self):
        error = "Invalid input data"
        result = self.classifier.classify_error(error)
        self.assertEqual(result, "validation")

    def test_classify_resource_error(self):
        error = "Resource not found"
        result = self.classifier.classify_error(error)
        self.assertEqual(result, "resource")

    def test_classify_unknown_error(self):
        error = "Unknown error occurred"
        result = self.classifier.classify_error(error)
        self.assertEqual(result, "unknown")

if __name__ == '__main__':
    unittest.main()