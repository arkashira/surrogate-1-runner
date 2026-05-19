CREATE TABLE IF NOT EXISTS cost_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP NOT NULL,
    resource_id TEXT NOT NULL,
    cost REAL NOT NULL,
    currency TEXT NOT NULL,
    service TEXT NOT NULL,
    UNIQUE(timestamp, resource_id)
);

CREATE INDEX IF NOT EXISTS idx_cost_records_resource ON cost_records(resource_id);
CREATE INDEX IF NOT EXISTS idx_cost_records_timestamp ON cost_records(timestamp);