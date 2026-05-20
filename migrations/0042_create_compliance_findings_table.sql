CREATE TABLE compliance_findings (
    id SERIAL PRIMARY KEY,
    resource_id VARCHAR(255) NOT NULL,
    resource_type VARCHAR(255) NOT NULL,
    rule_id VARCHAR(255) NOT NULL,
    rule_name VARCHAR(255) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'open',
    resolved_at TIMESTAMP
);