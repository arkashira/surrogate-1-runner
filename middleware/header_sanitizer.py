
import re
import time

def sanitize_headers(headers):
    # Remove original request headers and replace with sanitized metadata
    sanitized_headers = {
        'X-Sanitized-By': 'surrogate-1',
        'X-Request-Time': time.time(),
    }
    return sanitized_headers

def strip_and_sanitize(headers):
    # Strip original headers and apply sanitization
    for key in list(headers.keys()):
        if not re.match(r'^X-Sanitized-', key):
            del headers[key]
    return {**headers, **sanitize_headers(headers)}

# /opt/axentx/surrogate-1/worker.py

import requests

def send_request(url, headers, data):
    # Reroute requests through surrogate-1's worker
    headers = strip_and_sanitize(headers)
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# /opt/axentx/surrogate-1/test/test_header_sanitizer.py

import unittest
from middleware.header_sanitizer import strip_and_sanitize

class TestHeaderSanitizer(unittest.TestCase):

    def test_strip_and_sanitize(self):
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'X-Original-Header': 'some-value',
        }
        sanitized_headers = strip_and_sanitize(headers)
        self.assertNotIn('User-Agent', sanitized_headers)
        self.assertNotIn('X-Original-Header', sanitized_headers)
        self.assertIn('X-Sanitized-By', sanitized_headers)
        self.assertIn('X-Request-Time', sanitized_headers)

## Summary
- Implemented header sanitization logic in /opt/axentx/surrogate-1/middleware/header_sanitizer.py
- Updated /opt/axentx/surrogate-1/worker.py to reroute requests through the sanitized headers
- Added test case for header sanitization in /opt/axentx/surrogate-1/test/test_header_sanitizer.py