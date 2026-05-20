import unittest
from unittest.mock import patch
from datetime import datetime
from src.routes.events import post_event
from src.models import UserEvent, db

class TestEventsRoute(unittest.TestCase):

    @patch('src.routes.events.request')
    def test_post_event(self, mock_request):
        mock_request.json.return_value = {
            'user_id': 'test_user',
            'event_type': 'test_event',
            'payload': {'key': 'value'}
        }

        with patch.object(db.session, 'add') as mock_add, \
             patch.object(db.session, 'commit') as mock_commit:
            response = post_event()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Event recorded successfully"})
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()