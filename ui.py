from flask import Flask, request, jsonify, Response, stream_with_context
import threading
import time
import json
import uuid

app = Flask(__name__)

# In-memory stores for agents and workflows
agents = {}
workflows = {}
# Status store: {agent_id: {"status": str, "metrics": dict}}
statuses = {}

# Experience manager import
try:
    from .experience import ExperienceManager
except Exception:
    ExperienceManager = None

# Background thread to simulate real-time status updates
def status_updater():
    while True:
        for agent_id in agents:
            # Simulate status change
            statuses[agent_id] = {
                "status": "running" if time.time() % 2 < 1 else "idle",
                "metrics": {"cpu": round(50 + 10 * (time.time() % 1), 2)}
            }
        time.sleep(5)

threading.Thread(target=status_updater, daemon=True).start()

# Helper to stream Server-Sent Events
def event_stream():
    while True:
        for agent_id, status in statuses.items():
            data = json.dumps({"agent_id": agent_id, "status": status})
            yield f"data: {data}\n\n"
        time.sleep(5)

@app.route("/")
def index():
    return """
    <h1>Surrogate-1 Agent & Workflow Manager</h1>
    <p>Use the API endpoints to manage agents and workflows.</p>
    <ul>
        <li>GET /agents</li>
        <li>POST /agents</li>
        <li>GET /agents/&lt;id&gt;</li>
        <li>PUT /agents/&lt;id&gt;</li>
        <li>DELETE /agents/&lt;id&gt;</li>
        <li>GET /workflows</li>
        <li>POST /workflows</li>
        <li>GET /workflows/&lt;id&gt;</li>
        <li>PUT /workflows/&lt;id&gt;</li>
        <li>DELETE /workflows/&lt;id&gt;</li>
        <li>GET /status/stream (SSE)</li>
    </ul>
    """

# Agent endpoints
@app.route("/agents", methods=["GET", "POST"])
def agents_collection():
    if request.method == "GET":
        return jsonify(list(agents.values()))
    elif request.method == "POST":
        data = request.json or {}
        agent_id = str(uuid.uuid4())
        agent = {
            "id": agent_id,
            "name": data.get("name", f"Agent {agent_id}"),
            "config": data.get("config", {})
        }
        agents[agent_id] = agent
        statuses[agent_id] = {"status": "idle", "metrics": {}}
        return jsonify(agent), 201

@app.route("/agents/<agent_id>", methods=["GET", "PUT", "DELETE"])
def agent_detail(agent_id):
    agent = agents.get(agent_id)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    if request.method == "GET":
        return jsonify(agent)
    elif request.method == "PUT":
        data = request.json or {}
        agent["name"] = data.get("name", agent["name"])
        agent["config"] = data.get("config", agent["config"])
        return jsonify(agent)
    elif request.method == "DELETE":
        agents.pop(agent_id)
        statuses.pop(agent_id, None)
        return jsonify({"message": "Agent deleted"})

# Workflow endpoints
@app.route("/workflows", methods=["GET", "POST"])
def workflows_collection():
    if request.method == "GET":
        return jsonify(list(workflows.values()))
    elif request.method == "POST":
        data = request.json or {}
        wf_id = str(uuid.uuid4())
        workflow = {
            "id": wf_id,
            "name": data.get("name", f"Workflow {wf_id}"),
            "steps": data.get("steps", []),
            "config": data.get("config", {})
        }
        workflows[wf_id] = workflow
        return jsonify(workflow), 201

@app.route("/workflows/<wf_id>", methods=["GET", "PUT", "DELETE"])
def workflow_detail(wf_id):
    workflow = workflows.get(wf_id)
    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404
    if request.method == "GET":
        return jsonify(workflow)
    elif request.method == "PUT":
        data = request.json or {}
        workflow["name"] = data.get("name", workflow["name"])
        workflow["steps"] = data.get("steps", workflow["steps"])
        workflow["config"] = data.get("config", workflow["config"])
        return jsonify(workflow)
    elif request.method == "DELETE":
        workflows.pop(wf_id)
        return jsonify({"message": "Workflow deleted"})

# Real-time status stream (Server-Sent Events)
@app.route("/status/stream")
def status_stream():
    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream"
    )

# Optional: expose experience manager for customization
if ExperienceManager:
    exp_manager = ExperienceManager()
    @app.route("/experience", methods=["GET", "POST"])
    def experience():
        if request.method == "GET":
            return jsonify(exp_manager.get_preferences())
        elif request.method == "POST":
            prefs = request.json or {}
            exp_manager.set_preferences(prefs)
            return jsonify(exp_manager.get_preferences())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)