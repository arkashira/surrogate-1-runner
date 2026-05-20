CREATE TABLE costinel_monthly_snapshot (
    tenant_id VARCHAR(36) NOT NULL,
    snapshot_date DATE NOT NULL,
    total_spend NUMERIC(15,2) NOT NULL,
    service_breakdown JSONB NOT NULL,
    savings_recommendations JSONB NOT NULL,
    fetched_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tenant_id, snapshot_date)
);

CREATE INDEX idx_costinel_snapshot_fetched ON costinel_monthly_snapshot (fetched_at);
CREATE INDEX idx_costinel_service_breakdown_gin ON costinel_monthly_snapshot USING GIN (service_breakdown);
CREATE INDEX idx_costinel_savings_gin ON costinel_monthly_snapshot USING GIN (savings_recommendations);