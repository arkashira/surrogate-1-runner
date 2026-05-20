CREATE TABLE IF NOT EXISTS cost_records (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    resource_id VARCHAR(255) NOT NULL,
    provider VARCHAR(50) NOT NULL DEFAULT 'aws',
    cost_amount DECIMAL(18, 6) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    resource_type VARCHAR(100),
    service VARCHAR(100),
    region VARCHAR(50),
    tags JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (timestamp, resource_id)
);

CREATE INDEX idx_cost_records_timestamp ON cost_records(timestamp);
CREATE INDEX idx_cost_records_resource_id ON cost_records(resource_id);
CREATE INDEX idx_cost_records_provider ON cost_records(provider);
CREATE INDEX idx_cost_records_timestamp_provider ON cost_records(timestamp, provider);