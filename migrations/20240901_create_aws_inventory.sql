-- PostgreSQL migration for AWS inventory tracking

CREATE SCHEMA IF NOT EXISTS aws_inventory;

-- Core inventory metadata table
CREATE TABLE aws_inventory.metadata (
    id SERIAL PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(255) NOT NULL,
    region VARCHAR(50) NOT NULL,
    account_id VARCHAR(128) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_ingested_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(resource_type, resource_id, region, account_id)
);

-- Resource attributes table (denormalized for query performance)
CREATE TABLE aws_inventory.resource_attributes (
    id SERIAL PRIMARY KEY,
    metadata_id INTEGER NOT NULL REFERENCES aws_inventory.metadata(id) ON DELETE CASCADE,
    key VARCHAR(128) NOT NULL,
    value TEXT,
    raw_value JSONB,
    UNIQUE(metadata_id, key)
);

-- Ingestion tracking table
CREATE TABLE aws_inventory.ingestion_batches (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR(64) NOT NULL UNIQUE,
    resource_types TEXT[] NOT NULL,
    total_resources INTEGER NOT NULL DEFAULT 0,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    error_message TEXT
);

-- Indexes for common query patterns
CREATE INDEX idx_metadata_resource_lookup ON aws_inventory.metadata(resource_type, resource_id, region);
CREATE INDEX idx_metadata_account_lookup ON aws_inventory.metadata(account_id, resource_type);
CREATE INDEX idx_metadata_created ON aws_inventory.metadata(created_at DESC);
CREATE INDEX idx_metadata_updated ON aws_inventory.metadata(updated_at DESC);
CREATE INDEX idx_metadata_last_ingested ON aws_inventory.metadata(last_ingested_at DESC);

CREATE INDEX idx_attributes_lookup ON aws_inventory.resource_attributes(metadata_id, key);
CREATE INDEX idx_batch_lookup ON aws_inventory.ingestion_batches(ingested_at DESC);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION aws_inventory.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger on metadata table
CREATE TRIGGER update_metadata_updated_at
    BEFORE UPDATE ON aws_inventory.metadata
    FOR EACH ROW
    EXECUTE FUNCTION aws_inventory.update_updated_at();

-- Function to update updated_at for resource_attributes
CREATE OR REPLACE FUNCTION aws_inventory.update_attr_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger on resource_attributes table
CREATE TRIGGER update_attr_updated_at
    BEFORE UPDATE ON aws_inventory.resource_attributes
    FOR EACH ROW
    EXECUTE FUNCTION aws_inventory.update_attr_updated_at();

-- View for quick inventory summary by resource type
CREATE VIEW aws_inventory.resource_summary AS
SELECT 
    resource_type,
    COUNT(DISTINCT resource_id) AS total_count,
    COUNT(DISTINCT account_id) AS account_count,
    COUNT(DISTINCT region) AS region_count,
    MIN(created_at) AS first_seen,
    MAX(updated_at) AS last_seen
FROM aws_inventory.metadata
GROUP BY resource_type;

-- View for recent ingestion status
CREATE VIEW aws_inventory.ingestion_status AS
SELECT 
    batch_id,
    resource_types,
    total_resources,
    status,
    ingested_at,
    completed_at,
    EXTRACT(EPOCH FROM (completed_at - ingested_at)) AS duration_seconds
FROM aws_inventory.ingestion_batches
ORDER BY ingested_at DESC
LIMIT 100;