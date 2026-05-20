from pipeline_tracker import (
    PipelineTracker,
    ChangeType,
    ImpactLevel,
    get_impact_color,
    get_environment_color,
)

# Create a tracker (optionally pass persistence settings)
tracker = PipelineTracker(
    max_history=2000,
    persistence_file="tracker_state.json",   # or None
)

# Subscribe to live events
def on_change(change):
    print(f"[{change.impact.upper()}] {change.message}")

tracker.subscribe(on_change)

# Add a change
tracker.add_change(
    change_type=ChangeType.WORKFLOW_CHANGE,
    impact=ImpactLevel.CRITICAL,
    author="devops-bot",
    environment="production",
    message="Scaled runners from 8 → 16",
    details={"old": 8, "new": 16},
)

# Get recent events
recent = tracker.get_recent_changes(limit=10)

# Get JSON for a dashboard
dashboard_json = tracker.to_json()

# Optional: clear history
tracker.clear_history()