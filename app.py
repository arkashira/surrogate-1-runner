import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Flask, render_template, jsonify, g

app = Flask(__name__, template_folder=Path(__file__).parent / "templates")
app.config.update(
    DATABASE=Path(__file__).parent / "requests.db",
    SLA_ON_TRACK_H=24,
    SLA_AT_RISK_H=72,
    MAX_ROWS=1000,
    DAYS=30,
)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        # Enable WAL for concurrent reads/writes and better performance
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=NORMAL")
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_created ON requests(created_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON requests(status)")
    conn.commit()

def seed_demo_data():
    conn = get_db()
    if conn.execute("SELECT 1 FROM requests LIMIT 1").fetchone() is not None:
        return

    now = datetime.now(timezone.utc)
    rows = []
    statuses = ["pending", "processing", "completed", "failed", "cancelled"]
    for i in range(app.config["MAX_ROWS"]):
        created = now - timedelta(hours=i * 0.7, minutes=i % 60)
        updated = created + timedelta(hours=i % 48, minutes=i % 30)
        status = statuses[i % len(statuses)]
        rows.append((
            f"req-{10000 + i}",
            status,
            created.isoformat(),
            updated.isoformat(),
        ))
    conn.executemany(
        "INSERT INTO requests(request_id, status, created_at, updated_at) VALUES (?, ?, ?, ?)",
        rows,
    )
    conn.commit()

def _sla_state(updated_at_iso: str) -> str:
    updated = datetime.fromisoformat(updated_at_iso.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    age_h = (now - updated).total_seconds() / 3600.0
    if age_h <= app.config["SLA_ON_TRACK_H"]:
        return "on-track"
    if age_h <= app.config["SLA_AT_RISK_H"]:
        return "at-risk"
    return "breached"

@app.route("/dashboard/requests")
def dashboard_requests():
    conn = get_db()
    since = (datetime.now(timezone.utc) - timedelta(days=app.config["DAYS"])).isoformat()

    # Status counts (last N days)
    status_rows = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM requests WHERE created_at >= ? GROUP BY status",
        (since,),
    ).fetchall()
    status_counts = {r["status"]: r["cnt"] for r in status_rows}

    # SLA summary computed dynamically for last N days
    sla_rows = conn.execute(
        "SELECT updated_at FROM requests WHERE created_at >= ? ORDER BY created_at DESC LIMIT ?",
        (since, app.config["MAX_ROWS"]),
    ).fetchall()
    sla_counts = {"on-track": 0, "at-risk": 0, "breached": 0}
    for r in sla_rows:
        s = _sla_state(r["updated_at"])
        sla_counts[s] += 1

    # Recent rows for table (capped)
    recent_rows = conn.execute(
        "SELECT request_id, status, created_at, updated_at FROM requests "
        "WHERE created_at >= ? ORDER BY created_at DESC LIMIT ?",
        (since, app.config["MAX_ROWS"]),
    ).fetchall()

    recent = []
    for r in recent_rows:
        recent.append({
            "request_id": r["request_id"],
            "status": r["status"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "sla_state": _sla_state(r["updated_at"]),
        })

    return render_template(
        "dashboard.html",
        status_counts=status_counts,
        sla_summary=sla_counts,
        recent_requests=recent,
        total_recent=len(recent),
    )

@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok", "time_utc": datetime.now(timezone.utc).isoformat()})

# CLI helpers
import click
@click.group()
def cli():
    pass

@cli.command()
def initdb():
    """Initialize database and indexes."""
    init_db()
    click.echo("Database initialized.")

@cli.command()
def seed():
    """Seed demo data (only if empty)."""
    seed_demo_data()
    click.echo("Demo data seeded (if empty).")

@cli.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8080, type=int)
def run(host, port):
    """Run the dashboard server."""
    init_db()
    seed_demo_data()
    app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    cli()