import unittest
from src.parser.link_parser import LinkParser

class TestLinkParser(unittest.TestCase):
    def setUp(self):
        self.parser = LinkParser()

    def test_parse_links(self):
        text = "This is a [link](http://example.com) and another [one](http://example.org)"
        expected = [("link", "http://example.com"), ("one", "http://example.org")]
        self.assertEqual(self.parser.parse_links(text), expected)

    def test_parse_documents(self):
        documents = {
            "doc1.md": "This is a [link](http://example.com)",
            "doc2.md": "Another [link](http://example.org)"
        }
        expected = {
            "doc1.md": [("link", "http://example.com")],
            "doc2.md": [("one", "http://example.org")]
        }
        self.assertEqual(self.parser.parse_documents(documents), expected)

if __name__ == '__main__':
    unittest.main()