-- Add cloud_costs table
CREATE TABLE IF NOT EXISTS cloud_costs (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    service VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on provider and service columns
CREATE INDEX idx_cloud_costs_provider_service ON cloud_costs (provider, service);

-- Create index on timestamp column
CREATE INDEX idx_cloud_costs_timestamp ON cloud_costs (timestamp);