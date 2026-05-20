/* --------------------------------------------------------------
   File: migrations/20240604_create_cost_anomalies.sql
   Purpose: Store the results of cost‑anomaly detection so that
            downstream services can query, alert, and audit them.
   -------------------------------------------------------------- */

-- 1️⃣  Table definition -------------------------------------------------
CREATE TABLE cost_anomalies (
    ------------------------------------------------------------------
    -- Primary key
    id               SERIAL PRIMARY KEY,

    ------------------------------------------------------------------
    -- Link back to the raw cost record (if you have a `costs` table)
    cost_id          INT NOT NULL
                     REFERENCES costs(id)
                     ON DELETE CASCADE,

    ------------------------------------------------------------------
    -- When the source data was ingested (e.g. the billing day)
    ingestion_date   DATE NOT NULL,

    ------------------------------------------------------------------
    -- When the anomaly was detected by the model / pipeline
    detected_at      TIMESTAMP WITH TIME ZONE NOT NULL
                     DEFAULT CURRENT_TIMESTAMP,

    ------------------------------------------------------------------
    -- Monetary impact of the anomaly (optional but useful for triage)
    total_cost       NUMERIC(15,2) NOT NULL CHECK (total_cost >= 0),

    ------------------------------------------------------------------
    -- Human‑readable classification (e.g. “spike”, “outlier”, “missing”)
    anomaly_type     VARCHAR(50) NOT NULL,

    ------------------------------------------------------------------
    -- Model confidence – keep four decimal places so we can store 0.0001
    confidence_score NUMERIC(5,4) NOT NULL
                     CHECK (confidence_score >= 0 AND confidence_score <= 1),

    ------------------------------------------------------------------
    -- Free‑form description that the model (or a later enrichment step)
    -- can fill in.  `details` is kept for backward compatibility with the
    -- second proposal.
    anomaly_description TEXT,
    details          TEXT,

    ------------------------------------------------------------------
    -- URL to a generated PDF/HTML report (optional)
    report_url       TEXT,

    ------------------------------------------------------------------
    -- Alert / processing flags
    alert_sent       BOOLEAN NOT NULL DEFAULT FALSE,
    processed        BOOLEAN NOT NULL DEFAULT FALSE,

    ------------------------------------------------------------------
    -- Auditing columns
    created_at       TIMESTAMP WITH TIME ZONE NOT NULL
                     DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP WITH TIME ZONE NOT NULL
                     DEFAULT CURRENT_TIMESTAMP
);

-- 2️⃣  Indexes -----------------------------------------------------------
-- Fast look‑ups by the most common filter dimensions
CREATE INDEX idx_cost_anomalies_cost_id
    ON cost_anomalies(cost_id);

CREATE INDEX idx_cost_anomalies_ingestion_date
    ON cost_anomalies(ingestion_date);

CREATE INDEX idx_cost_anomalies_detected_at
    ON cost_anomalies(detected_at);

CREATE INDEX idx_cost_anomalies_processed
    ON cost_anomalies(processed);

CREATE INDEX idx_cost_anomalies_alert_sent
    ON cost_anomalies(alert_sent);

-- 3️⃣  Triggers -----------------------------------------------------------
-- Keep `updated_at` in sync automatically
CREATE OR REPLACE FUNCTION trg_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_cost_anomalies_upd
BEFORE UPDATE ON cost_anomalies
FOR EACH ROW EXECUTE FUNCTION trg_update_timestamp();