CREATE TABLE IF NOT EXISTS cost_anomalies (
    id BIGSERIAL PRIMARY KEY,
    service TEXT NOT NULL,
    anomaly_hour TIMESTAMPTZ NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('LOW', 'HIGH')),
    rolling_avg NUMERIC(15, 4) NOT NULL,
    actual_spend NUMERIC(15, 4) NOT NULL,
    multiplier NUMERIC(5, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    UNIQUE (service, anomaly_hour)
);

CREATE INDEX idx_cost_anomalies_service ON cost_anomalies(service);
CREATE INDEX idx_cost_anomalies_anomaly_hour ON cost_anomalies(anomaly_hour);
CREATE INDEX idx_cost_anomalies_severity ON cost_anomalies(severity);
CREATE INDEX idx_cost_anomalies_created_at ON cost_anomalies(created_at);

COMMENT ON TABLE cost_anomalies IS 'Stores hourly cost anomalies where spend exceeds rolling 7-day average';
COMMENT ON COLUMN cost_anomalies.severity IS 'LOW: 2-3x average, HIGH: >3x average';
COMMENT ON COLUMN cost_anomalies.rolling_avg IS '7-day rolling average spend for this service';
COMMENT ON COLUMN cost_anomalies.actual_spend IS 'Actual spend for this hour';
COMMENT ON COLUMN cost_anomalies.multiplier IS 'Ratio of actual_spend / rolling_avg';