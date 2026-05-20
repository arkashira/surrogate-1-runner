from flask import Blueprint, request, jsonify
from .db import get_conn
from .utils import hash_password

bp = Blueprint("register", __name__)

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    with get_conn() as conn:
        cur = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            return jsonify({"error": "username already taken"}), 409

        password_hash = hash_password(password).decode("utf-8")
        conn.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        conn.commit()

    return jsonify({"message": "user created"}), 201