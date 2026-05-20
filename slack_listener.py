"""
Slack Webhook Listener for Surrogate-1
Production-ready webhook handler with proper security verification.
"""

import json
import os
import hmac
import hashlib
import time
import logging
from typing import Dict, Any, Optional, Callable
from flask import Flask, request, jsonify, Response

logger = logging.getLogger(__name__)
app = Flask(__name__)

# Configuration
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET', '')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN', '')
SLACK_VERIFICATION_TOKEN = os.environ.get('SLACK_VERIFICATION_TOKEN', '')
SIGNATURE_TOLERANCE = 300  # 5 minutes

# Store for handler callbacks
_slack_handler: Optional[Any] = None


def set_handler(handler) -> None:
    """Set the Slack handler instance for processing events."""
    global _slack_handler
    _slack_handler = handler


def verify_slack_request(headers: Dict[str, str], body: str) -> bool:
    """
    Verify that the request came from Slack using the signing secret.
    Implements HMAC-SHA256 verification per Slack docs.
    """
    if not SLACK_SIGNING_SECRET:
        logger.warning("SLACK_SIGNING_SECRET not configured, skipping verification")
        return True
    
    signature = headers.get('X-Slack-Signature', '')
    timestamp = headers.get('X-Slack-Request-Timestamp', '')
    
    if not signature or not timestamp:
        logger.warning("Missing Slack verification headers")
        return False
    
    # Reject requests older than 5 minutes
    if abs(time.time() - int(timestamp)) > SIGNATURE_TOLERANCE:
        logger.warning("Request timestamp outside tolerance window")
        return False
    
    # Compute expected signature
    base_string = f"v0:{timestamp}:{body}"
    expected_signature = 'v0=' + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        base_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)


def require_verification(f: Callable) -> Callable:
    """Decorator to require Slack request verification."""
    def decorated(*args, **kwargs):
        body = request.get_data(as_text=True)
        if not verify_slack_request(dict(request.headers), body):
            logger.warning(f"Verification failed for request from {request.remote_addr}")
            return jsonify({'error': 'Verification failed'}), 401
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


@app.route('/webhooks/slack', methods=['GET', 'POST'])
@require_verification
def slack_webhook():
    """Main Slack webhook endpoint."""
    if request.method == 'GET':
        return jsonify({'status': 'ok', 'service': 'slack-webhook-listener'})
    
    data = request.get_json(silent=True) or {}
    logger.info(f"Received Slack webhook: {json.dumps(data, default=str)[:500]}")
    
    # Handle URL verification challenge
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data.get('challenge', '')})
    
    # Handle event callbacks
    if data.get('type') == 'event_callback':
        event = data.get('event', {})
        event_type = event.get('type')
        
        if _slack_handler:
            try:
                _slack_handler.handle_event(event_type, event)
            except Exception as e:
                logger.exception(f"Error handling Slack event: {e}")
                return jsonify({'error': str(e)}), 500
        
        return jsonify({'status': 'ok'})
    
    # Handle interactive components
    if data.get('type') in ['block_actions', 'view_submission', 'shortcut', 'message_action']:
        if _slack_handler:
            try:
                _slack_handler.handle_interaction(data)
            except Exception as e:
                logger.exception(f"Error handling Slack interaction: {e}")
                return jsonify({'error': str(e)}), 500
        
        return jsonify({'status': 'ok'})
    
    return jsonify({'status': 'received'})


@app.route('/webhooks/slack/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'slack-webhook-listener',
        'handler_loaded': _slack_handler is not None,
        'verification_configured': bool(SLACK_SIGNING_SECRET)
    })


def create_app():
    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)