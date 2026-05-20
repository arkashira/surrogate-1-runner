"""
A tiny helper that patches `requests.post` so that any outbound call
from the webhook (e.g. to GitLab) is intercepted and returns a
controlled response.

It is intentionally simple – you can replace it with `responses`,
`httpretty`, or `requests-mock` if you need more features.
"""

import json
from unittest.mock import patch, Mock

class MockGitlabServer:
    """
    Usage:

        with MockGitlabServer() as mock:
            mock.post.return_value.json.return_value = {...}
            # run your code that triggers requests.post(...)
    """

    def __init__(self):
        self._patcher = patch("requests.post")
        self.post = self._patcher.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._patcher.stop()