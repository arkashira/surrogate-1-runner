import unittest
from flask import Flask, jsonify
from middleware import api_key_required

app = Flask(__name__)

@app.route('/secure-data', methods=['GET'])
@api_key_required
def secure_data():
    return jsonify({"data": "This is secured data."})

class MiddlewareTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_access_with_valid_api_key(self):
        response = self.app.get('/secure-data', headers={'X-API-KEY': 'your_api_key_1'})
        self.assertEqual(response.status_code, 200)

    def test_access_with_invalid_api_key(self):
        response = self.app.get('/secure-data', headers={'X-API-KEY': 'invalid_key'})
        self.assertEqual(response.status_code, 401)

    def test_access_without_api_key(self):
        response = self.app.get('/secure-data')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()