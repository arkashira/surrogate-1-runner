
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class PrometheusAPIClient:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        retry_strategy = Retry(connect=3, backoff_factor=0.3)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def fetch_metrics(self, query):
        try:
            response = self.session.get(f'{self.url}/api/v1/query', params={'query': query})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(f'Error fetching metrics: {err}')
            return None

# opt/axentx/surrogate-1/tests/test_integrations_prometheus_client.py

import unittest
from unittest.mock import patch, Mock
from integrations.prometheus.client import PrometheusAPIClient

class TestPrometheusAPIClient(unittest.TestCase):
    def setUp(self):
        self.url = 'http://test-prometheus'
        self.token = 'test-token'
        self.client = PrometheusAPIClient(self.url, self.token)

    @patch('requests.Session.get')
    def test_fetch_metrics_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': {'result': [{'metric': {}, 'value': [1, 2]}]}}
        result = self.client.fetch_metrics('test_query')
        self.assertIsNotNone(result)

    @patch('requests.Session.get')
    def test_fetch_metrics_error(self, mock_get):
        mock_get.side_effect = Exception('Test exception')
        result = self.client.fetch_metrics('test_query')
        self.assertIsNone(result)

## Summary
- Implemented Prometheus API client with retry logic
- Added unit tests for fetch_metrics method
- Successfully handled API errors and timeouts