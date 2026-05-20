from flask import Blueprint, request, jsonify
from datetime import datetime
from .auth import requires_auth, check_permissions
from .models import Lock, Document, Section

locks_bp = Blueprint('locks', __name__)

@locks_bp.route('/api/locks', methods=['GET'])
@requires_auth
def get_locks():
    doc_id = request.args.get('doc_id')
    user = request.user  # Assuming request.user contains the authenticated user info
    
    # Check if the user has permission to view lock owners
    if not check_permissions(user, ['owner', 'admin']):
        return jsonify({"error": "Permission denied"}), 403

    try:
        document = Document.query.get(doc_id)
        if not document:
            return jsonify([]), 200

        active_locks = Lock.query.filter_by(document_id=doc_id, is_active=True).all()
        
        lock_list = []
        for lock in active_locks:
            section = Section.query.get(lock.section_id)
            lock_info = {
                "owner": lock.owner,
                "section_range": f"{lock.start}-{lock.end}",
                "expiry": lock.expiry.isoformat(),
                "section_title": section.title if section else "Unknown"
            }
            lock_list.append(lock_info)

        return jsonify(lock_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# /opt/axentx/surrogate-1/tests/test_locks.py
import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from api.locks import get_locks

class TestLocksEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    @patch('api.locks.Document.query')
    @patch('api.locks.Lock.query')
    @patch('api.locks.Section.query')
    @patch('api.locks.request')
    def test_get_locks_with_valid_doc_id(self, mock_request, mock_section_query, mock_lock_query, mock_document_query):
        mock_request.args.get.return_value = 'valid_doc_id'
        mock_document_query.get.return_value = MagicMock(id='valid_doc_id')
        mock_lock_query.filter_by.return_value.all.return_value = [
            MagicMock(owner='owner1', start=1, end=10, expiry=datetime.now(), section_id='section1', is_active=True),
            MagicMock(owner='owner2', start=11, end=20, expiry=datetime.now(), section_id='section2', is_active=True)
        ]
        mock_section_query.get.side_effect = [MagicMock(title='Section 1'), MagicMock(title='Section 2')]

        response = get_locks()
        data = response[0].json

        expected_data = [
            {
                "owner": "owner1",
                "section_range": "1-10",
                "expiry": mock_lock_query.filter_by.return_value.all.return_value[0].expiry.isoformat(),
                "section_title": "Section 1"
            },
            {
                "owner": "owner2",
                "section_range": "11-20",
                "expiry": mock_lock_query.filter_by.return_value.all.return_value[1].expiry.isoformat(),
                "section_title": "Section 2"
            }
        ]

        self.assertEqual(data, expected_data)
        self.assertEqual(response[1], 200)

    @patch('api.locks.Document.query')
    @patch('api.locks.Lock.query')
    @patch('api.locks.request')
    def test_get_locks_with_no_locks(self, mock_request, mock_lock_query, mock_document_query):
        mock_request.args.get.return_value = 'valid_doc_id'
        mock_document_query.get.return_value = MagicMock(id='valid_doc_id')
        mock_lock_query.filter_by.return_value.all.return_value = []

        response = get_locks()
        data = response[0].json

        self.assertEqual(data, [])
        self.assertEqual(response[1], 200)

    @patch('api.locks.check_permissions')
    @patch('api.locks.request')
    def test_get_locks_permission_denied(self, mock_request, mock_check_permissions):
        mock_request.user = MagicMock()
        mock_check_permissions.return_value = False

        response = get_locks()
        data = response[0].json

        self.assertEqual(data, {"error": "Permission denied"})
        self.assertEqual(response[1], 403)


## Summary
- Added `/api/locks` endpoint to list active locks.
- Included lock owner, section range, expiry, and section title in response.
- Implemented permission checks for lock owners and admins.
- Added unit tests for the new endpoint functionality.