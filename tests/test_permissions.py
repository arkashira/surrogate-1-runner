import unittest
from flask import Flask, jsonify
from middleware.permissions import permission_required

class TestPermissions(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

        @self.app.route('/admin', methods=['GET'])
        @permission_required('admin')
        def admin_route():
            return jsonify({'message': 'Welcome, admin!'})

        @self.app.route('/protected', methods=['GET'])
        @permission_required('engineer')
        def protected_route():
            return jsonify({'message': 'You have access to this route!'})

    def test_admin_access(self):
        response = self.client.get('/admin', headers={'X-Username': 'user1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Welcome, admin!'})

    def test_engineer_access(self):
        response = self.client.get('/protected', headers={'X-Username': 'user2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'You have access to this route!'})

    def test_access_denied(self):
        response = self.client.get('/protected', headers={'X-Username': 'user3'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'error': 'Access denied'})

    def test_user_not_found(self):
        response = self.client.get('/protected', headers={'X-Username': 'unknown_user'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'error': 'User not found'})

if __name__ == '__main__':
    unittest.main()