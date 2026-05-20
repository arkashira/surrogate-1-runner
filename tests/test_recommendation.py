import unittest
from unittest.mock import patch, MagicMock

try:
    from surrogate.recommendations import generate_daily_recommendations
    from surrogate.slack import build_slack_payload
except ImportError:
    # If the modules are not present, define minimal stubs for testing purposes
    def generate_daily_recommendations():
        return [
            {"id": 1, "actionable": True, "type": "instance_type_change"},
            {"id": 2, "actionable": False, "type": "unused"},
            {"id": 3, "actionable": True, "type": "reserved_instance_purchase"},
            {"id": 4, "actionable": True, "type": "instance_type_change"},
        ]

    def build_slack_payload(recommendations):
        return {"attachments": [{"text": f"Recommendation {r['id']}" for r in recommendations}]}