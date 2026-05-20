import unittest
import json
from src.main.endpoints import app, metrics_store

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        metrics_store.redis_client.flushall()

    def test_post_event(self):
        response = self.client.post('/api/v1/events', json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('event_id', data)

    def test_post_metric(self):
        metric_data = {
            'metric': 'test_metric',
            'type': 'gauge',
            'value': 10.5
        }
        response = self.client.post('/api/v1/series', json=metric_data)
        self.assertEqual(response.status_code, 200)

    def test_get_metrics(self):
        metric_data = {
            'metric': 'test_metric',
            'type': 'gauge',
            'value': 10.5
        }
        self.client.post('/api/v1/series', json=metric_data)
        response = self.client.get('/api/v1/series?metric=test_metric')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('gauge', data)
        self.assertIn(10.5, data['gauge'])

if __name__ == '__main__':
    unittest.main()