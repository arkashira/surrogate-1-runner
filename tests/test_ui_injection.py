import unittest
from unittest.mock import patch, MagicMock
from surrogate_1.ui_injection import inject_navigation_bar, fetch_site_map

class TestUIInjection(unittest.TestCase):

    @patch('surrogate_1.ui_injection.requests.get')
    def test_fetch_site_map(self, mock_get):
        """
        Tests if the fetch_site_map function correctly fetches and parses the site map data.
        """
        # Mock the response from the site map API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "hierarchy": [
                {"name": "Home", "url": "/home"},
                {"name": "Courses", "url": "/courses"},
                {"name": "About", "url": "/about"}
            ]
        }
        mock_get.return_value = mock_response

        # Call the function
        site_map = fetch_site_map()

        # Assert the response is as expected
        expected_hierarchy = [
            {"name": "Home", "url": "/home"},
            {"name": "Courses", "url": "/courses"},
            {"name": "About", "url": "/about"}
        ]
        self.assertEqual(site_map['hierarchy'], expected_hierarchy)

    @patch('surrogate_1.ui_injection.fetch_site_map')
    def test_inject_navigation_bar(self, mock_fetch_site_map):
        """
        Tests if the inject_navigation_bar function correctly injects the navigation bar into the HTML response.
        """
        # Mock the site map data
        mock_fetch_site_map.return_value = {
            "hierarchy": [
                {"name": "Home", "url": "/home"},
                {"name": "Courses", "url": "/courses"},
                {"name": "About", "url": "/about"}
            ]
        }

        # Mock the response object
        mock_response = MagicMock()
        mock_response.content = b'<html><body></body></html>'

        # Call the function
        result = inject_navigation_bar(mock_response)

        # Assert the navigation bar is injected
        decoded_content = result.content.decode('utf-8')
        self.assertIn('<nav id="navigation-bar">', decoded_content)
        self.assertIn('<a href="/home">Home</a>', decoded_content)
        self.assertIn('<a href="/courses">Courses</a>', decoded_content)
        self.assertIn('<a href="/about">About</a>', decoded_content)

if __name__ == '__main__':
    unittest.main()