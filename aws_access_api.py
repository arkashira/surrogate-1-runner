import os
import json
import datetime
from typing import Dict, Any

from flask import Flask, request, jsonify, abort
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Configuration via environment variables
ROLE_ARN = os.getenv("AWS_ACCESS_ROLE_ARN")
SESSION_NAME = os.getenv("AWS_ACCESS_SESSION_NAME", "SurrogateAccessSession")
DURATION_SECONDS = int(os.getenv("AWS_ACCESS_DURATION_SECONDS", "3600"))
AUTH_TOKEN = os.getenv("AWS_ACCESS_AUTH_TOKEN")  # simple bearer token for auth

if not ROLE_ARN or not AUTH_TOKEN:
    raise RuntimeError(
        "AWS_ACCESS_ROLE_ARN and AWS_ACCESS_AUTH_TOKEN must be set in environment"
    )

app = Flask(__name__)

def _validate_token(token: str) -> bool:
    """
    Very simple token validation. In production, replace with a proper auth mechanism.
    """
    return token == AUTH_TOKEN

def _assume_role() -> Dict[str, Any]:
    """
    Call AWS STS to assume the configured role and return temporary credentials.
    """
    sts_client = boto3.client("sts")
    try:
        response = sts_client.assume_role(
            RoleArn=ROLE_ARN,
            RoleSessionName=SESSION_NAME,
            DurationSeconds=DURATION_SECONDS,
        )
    except (BotoCoreError, ClientError) as exc:
        app.logger.error("Failed to assume role: %s", exc)
        raise RuntimeError("Failed to assume role") from exc

    creds = response["Credentials"]
    return {
        "AccessKeyId": creds["AccessKeyId"],
        "SecretAccessKey": creds["SecretAccessKey"],
        "SessionToken": creds["SessionToken"],
        "Expiration": creds["Expiration"].isoformat(),
    }

@app.route("/access", methods=["GET"])
def access():
    """
    Endpoint to obtain temporary AWS credentials.
    Requires Authorization: Bearer <token>
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        abort(401, description="Missing or malformed Authorization header")

    token = auth_header.split(" ", 1)[1]
    if not _validate_token(token):
        abort(403, description="Invalid token")

    try:
        creds = _assume_role()
    except RuntimeError as exc:
        abort(500, description=str(exc))

    return jsonify(creds), 200

if __name__ == "__main__":
    # For local debugging; in production use a WSGI server
    app.run(host="0.0.0.0", port=5000, threaded=True)