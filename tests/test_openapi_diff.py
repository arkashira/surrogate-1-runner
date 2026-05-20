import json
import unittest
from openapi_diff import OpenAPIDiff  # Assuming OpenAPIDiff is the class responsible for diffing

class TestOpenAPIDiff(unittest.TestCase):
    def setUp(self):
        self.diff_engine = OpenAPIDiff()

    def test_diff_added_endpoint(self):
        old_spec = {
            "paths": {
                "/old-endpoint": {
                    "get": {
                        "summary": "Old endpoint"
                    }
                }
            }
        }
        new_spec = {
            "paths": {
                "/old-endpoint": {
                    "get": {
                        "summary": "Old endpoint"
                    }
                },
                "/new-endpoint": {
                    "get": {
                        "summary": "New endpoint"
                    }
                }
            }
        }
        diff = self.diff_engine.compare(old_spec, new_spec)
        expected_diff = {
            "added": ["/new-endpoint"],
            "removed": [],
            "modified": []
        }
        self.assertEqual(diff, expected_diff)

    def test_diff_removed_endpoint(self):
        old_spec = {
            "paths": {
                "/old-endpoint": {
                    "get": {
                        "summary": "Old endpoint"
                    }
                }
            }
        }
        new_spec = {
            "paths": {}
        }
        diff = self.diff_engine.compare(old_spec, new_spec)
        expected_diff = {
            "added": [],
            "removed": ["/old-endpoint"],
            "modified": []
        }
        self.assertEqual(diff, expected_diff)

    def test_diff_modified_endpoint_summary(self):
        old_spec = {
            "paths": {
                "/endpoint": {
                    "get": {
                        "summary": "Old summary"
                    }
                }
            }
        }
        new_spec = {
            "paths": {
                "/endpoint": {
                    "get": {
                        "summary": "New summary"
                    }
                }
            }
        }
        diff = self.diff_engine.compare(old_spec, new_spec)
        expected_diff = {
            "added": [],
            "removed": [],
            "modified": ["/endpoint"]
        }
        self.assertEqual(diff, expected_diff)

    def test_diff_modified_endpoint_method(self):
        old_spec = {
            "paths": {
                "/endpoint": {
                    "get": {
                        "summary": "Old summary"
                    }
                }
            }
        }
        new_spec = {
            "paths": {
                "/endpoint": {
                    "post": {
                        "summary": "New summary"
                    }
                }
            }
        }
        diff = self.diff_engine.compare(old_spec, new_spec)
        expected_diff = {
            "added": [],
            "removed": [],
            "modified": ["/endpoint"]
        }
        self.assertEqual(diff, expected_diff)

    def test_diff_modified_endpoint_parameters(self):
        old_spec = {
            "paths": {
                "/endpoint": {
                    "get": {
                        "parameters": [
                            {"name": "param1", "in": "query", "required": True}
                        ]
                    }
                }
            }
        }
        new_spec = {
            "paths": {
                "/endpoint": {
                    "get": {
                        "parameters": [
                            {"name": "param1", "in": "query", "required": True},
                            {"name": "param2", "in": "query", "required": False}
                        ]
                    }
                }
            }
        }
        diff = self.diff_engine.compare(old_spec, new_spec)
        expected_diff = {
            "added": [],
            "removed": [],
            "modified": ["/endpoint"]
        }
        self.assertEqual(diff, expected_diff)

    def test_diff_modified_endpoint_responses(self):
        old_spec = {
            "paths": {
                "/endpoint": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Old response"
                            }
                        }
                    }
                }
            }
        }
        new_spec = {
            "paths": {
                "/endpoint": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "New response"
                            },
                            "404": {
                                "description": "Not found"
                            }
                        }
                    }
                }
            }
        }
        diff = self.diff_engine.compare(old_spec, new_spec)
        expected_diff = {
            "added": [],
            "removed": [],
            "modified": ["/endpoint"]
        }
        self.assertEqual(diff, expected_diff)

if __name__ == '__main__':
    unittest.main()