-- Migration to create the audit_log table with tamper‑evident fields.
-- This migration is idempotent; it will not fail if the table already exists.

CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    decision VARCHAR(20) NOT NULL CHECK (decision IN ('approved', 'rejected')),
    timestamp TIMESTAMPTZ NOT NULL,
    approver_ip_masked VARCHAR(45) NOT NULL,
    audit_record_link VARCHAR(512) NOT NULL,
    hash CHAR(64) NOT NULL,
    prev_hash CHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    CONSTRAINT uq_file_timestamp UNIQUE (file_name, timestamp)
);

-- Indexes for efficient querying.
CREATE INDEX IF NOT EXISTS idx_audit_log_file_name ON audit_log (file_name);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log (timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_log_hash ON audit_log (hash);

-- Trigger to update updated_at on row modification
CREATE OR REPLACE FUNCTION audit_log_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_audit_log_update_timestamp ON audit_log;
CREATE TRIGGER trg_audit_log_update_timestamp
BEFORE UPDATE ON audit_log
FOR EACH ROW EXECUTE FUNCTION audit_log_update_timestamp();