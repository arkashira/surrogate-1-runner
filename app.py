import json, random, time
from datetime import datetime
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)                     # Allow front‑end on another port
socketio = SocketIO(app, cors_allowed_origins="*")

# --- In‑memory state (replace with DB in prod) ---
state = {
    "EC2": {"instances": [...], "last_updated": datetime.utcnow().isoformat()},
    "S3":   {"buckets":   [...], "last_updated": datetime.utcnow().isoformat()},
    # … other services …
}

def random_ec2_status():
    for i in state["EC2"]["instances"]:
        if random.random() < 0.1:
            i["status"] = random.choice(["running","stopped","pending"])

def random_lambda_invocations():
    for f in state["Lambda"]["functions"]:
        f["invocations"] += random.randint(1, 100)
        f["errors"] += random.randint(0, 2)

# Background thread that pushes diffs
def updater():
    while True:
        time.sleep(5)
        random_ec2_status()
        random_lambda_invocations()
        now = datetime.utcnow().isoformat()
        for svc in state:
            state[svc]["last_updated"] = now
        socketio.emit("diff", state, broadcast=True)

socketio.start_background_task(updater)

# REST endpoint – initial payload
@app.route("/api/state")
def get_state():
    return jsonify(state)

# Auth guard (simplified)
@app.before_request
def check_auth():
    if request.endpoint == "static" or request.path.startswith("/api/"):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token or not validate_token(token):
            return jsonify({"error":"unauth"}), 401

def validate_token(token: str) -> bool:
    # TODO: call Cognito / JWKS endpoint
    return True

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)