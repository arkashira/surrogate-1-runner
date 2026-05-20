from flask import Flask, request, jsonify
from src.settings import GITLAB_TOKEN

app = Flask(__name__)

class GitlabWebhook:
    """Encapsulates token validation and payload handling."""

    def __init__(self, token: str = GITLAB_TOKEN):
        self.expected_token = token

    def validate_token(self) -> bool:
        """Return True if the request header matches the expected token."""
        header_token = request.headers.get("X-Gitlab-Token")
        return header_token == self.expected_token

    def handle_request(self):
        """Process the incoming GitLab webhook."""
        if not self.validate_token():
            return jsonify({"error": "Invalid token"}), 401

        payload = request.get_json(silent=True) or {}
        merge_request = payload.get("merge_request")
        if not merge_request or "id" not in merge_request:
            return jsonify({"error": "Missing merge_request.id"}), 400

        # In a real app you would enqueue the event, trigger CI, etc.
        return jsonify({"merge_request_id": merge_request["id"]}), 200

@app.route("/surrogate-1/webhooks/gitlab", methods=["POST"])
def gitlab_webhook():
    """Flask entry point."""
    webhook = GitlabWebhook()
    return webhook.handle_request()