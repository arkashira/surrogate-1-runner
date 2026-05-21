"""
Minimal GitHub App OAuth and webhook integration for surrogate-1.

This module provides:
- Manifest generation for GitHub App installation.
- OAuth flow helpers (URL generation, code exchange).
- In-memory token storage (replace with persistent store in prod).
- A simple webhook handler that posts inline comments on PRs.

Dependencies:
- PyGithub (pip install PyGithub)
- python-dotenv (optional, for loading env vars)
"""

import os
import json
import secrets
import base64
from typing import Dict, Any, Optional

import requests
from github import Github, GithubException

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# These should be set in the environment or via a .env file.
GITHUB_APP_ID: str = os.getenv("GITHUB_APP_ID", "")
GITHUB_PRIVATE_KEY: str = os.getenv("GITHUB_PRIVATE_KEY", "")  # PEM string
GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")
OAUTH_REDIRECT_URI: str = os.getenv("OAUTH_REDIRECT_URI", "https://example.com/github/callback")
WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "supersecret")

# In-memory token store (user_id -> access_token). Replace with DB in prod.
_token_store: Dict[str, str] = {}

# --------------------------------------------------------------------------- #
# Manifest generation
# --------------------------------------------------------------------------- #

def create_manifest() -> Dict[str, Any]:
    """
    Return a JSON manifest for creating a new GitHub App.
    The manifest can be posted to https://github.com/settings/apps/new?private_key=...
    """
    if not GITHUB_APP_ID or not GITHUB_PRIVATE_KEY:
        raise ValueError("GITHUB_APP_ID and GITHUB_PRIVATE_KEY must be set")

    manifest = {
        "name": "Axentx Surrogate App",
        "url": "https://example.com",
        "redirect_url": OAUTH_REDIRECT_URI,
        "description": "Posts security findings as inline PR comments.",
        "default_permissions": {
            "pull_requests": "write",
            "issues": "write",
            "contents": "read",
        },
        "default_events": ["pull_request"],
        "public": False,
        "hooks": {
            "url": "https://example.com/github/webhook",
            "secret": WEBHOOK_SECRET,
            "insecure_ssl": "0",
        },
    }
    return manifest

# --------------------------------------------------------------------------- #
# OAuth helpers
# --------------------------------------------------------------------------- #

def get_oauth_url(state: Optional[str] = None) -> str:
    """
    Construct the GitHub OAuth authorization URL.
    """
    if not GITHUB_CLIENT_ID:
        raise ValueError("GITHUB_CLIENT_ID must be set")
    if state is None:
        state = secrets.token_urlsafe(16)
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": OAUTH_REDIRECT_URI,
        "state": state,
        "scope": "repo",
    }
    query = "&".join(f"{k}={requests.utils.quote(v)}" for k, v in params.items())
    return f"https://github.com/login/oauth/authorize?{query}"

def exchange_code(code: str) -> str:
    """
    Exchange the OAuth code for an access token.
    Returns the access token string.
    """
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        raise ValueError("OAuth client credentials must be set")
    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": OAUTH_REDIRECT_URI,
    }
    headers = {"Accept": "application/json"}
    resp = requests.post(token_url, data=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"GitHub OAuth error: {data.get('error_description')}")
    return data["access_token"]

def store_token(user_id: str, token: str) -> None:
    """
    Persist the user's access token. In production, replace with a database.
    """
    _token_store[user_id] = token

def get_token(user_id: str) -> Optional[str]:
    return _token_store.get(user_id)

def get_github_client(token: str) -> Github:
    """
    Return a PyGithub client authenticated with the given token.
    """
    return Github(token)

# --------------------------------------------------------------------------- #
# Webhook handling
# --------------------------------------------------------------------------- #

def verify_webhook_signature(payload_body: bytes, signature_header: str) -> bool:
    """
    Verify the HMAC SHA1 signature of the incoming webhook.
    """
    import hmac, hashlib
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=payload_body, digestmod=hashlib.sha1)
    expected = f"sha1={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature_header)

def handle_pr_webhook(payload: Dict[str, Any], user_id: str) -> None:
    """
    Process a pull_request event payload and post inline comments for each finding.
    This is a simplified example; real logic would parse findings from a scan result.

    :param payload: The JSON payload from GitHub.
    :param user_id: The user ID associated with the access token.
    """
    if not payload or not "pull_request" not in payload:
        return

    github = get_github_client(get_token(user_id))
    pr = github.get_pull_request(payload["pull_request"]["number"])
    if pr is None:
        return

    # Simplified example: post a comment with a hardcoded finding.
    comment = f"Security finding: {pr.title} contains sensitive data."
    pr.create_comment(comment)