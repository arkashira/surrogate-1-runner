import unittest
from unittest.mock import patch
from src.middleware.rate_limit import rate_limit
from flask import Flask, request

app = Flask(__name__)

@app.route('/test')
@rate_limit(limit=10, period=60)
def test_route():
    return "OK"

class TestRateLimit(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    @patch('src.middleware.rate_limit.redis_client')
    def test_rate_limit(self, mock_redis):
        mock_redis.zcard.return_value = 0
        mock_redis.zadd.return_value = None
        mock_redis.expire.return_value = True
        mock_redis.zremrangebyscore.return_value = 0
        
        response = self.client.get('/test', headers={'X-API-Key': 'test-key'})
        self.assertEqual(response.status_code, 200)
        
        mock_redis.zcard.return_value = 10
        response = self.client.get('/test', headers={'X-API-Key': 'test-key'})
        self.assertEqual(response.status_code, 429)

if __name__ == '__main__':
    unittest.main()