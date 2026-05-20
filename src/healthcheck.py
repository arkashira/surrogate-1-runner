#!/usr/bin/env python3
"""
A minimal Flask app that serves a health‑check endpoint.

This file is executed by the `web` service in the compose file.
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="OK"), 200

if __name__ == "__main__":
    # Expose on all interfaces so Docker can reach it
    app.run(host="0.0.0.0", port=5000)