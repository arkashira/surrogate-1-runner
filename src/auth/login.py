from flask import Blueprint, request, jsonify
from .db import get_conn
from .utils import verify_password, generate_token, token_expiry
from datetime import datetime

bp = Blueprint("login", __name__)

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, password_hash FROM users WHERE username = ?", (username,)
        )
        row = cur.fetchone()
        if not row or not verify_password(password, row["password_hash"].encode()):
            return jsonify({"error": "invalid credentials"}), 401

        token = generate_token()
        expires_at = token_expiry()
        conn.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, row["id"], expires_at),
        )
        conn.commit()

    return jsonify({"token": token, "expires_at": expires_at}), 200