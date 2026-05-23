
CREATE TABLE IF NOT EXISTS analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_requests INTEGER,
    per_model_counts TEXT,
    average_latency FLOAT
);