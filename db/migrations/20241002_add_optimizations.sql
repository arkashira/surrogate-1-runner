-- ==============================================================
--  /opt/axentx/surrogate-1/db/migrations/20241002_add_optimizations.sql
--  Migration: Add optimizations audit table for EC2 rightsizing
--  Author:   <your name>
--  Date:     2024‑10‑02
-- ==============================================================

-- --------------------------------------------------------------
-- 1️⃣  Enable pgcrypto for gen_random_uuid()
-- --------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- --------------------------------------------------------------
-- 2️⃣  Table definition
-- --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS optimizations (
    -- Primary key – UUID is the safest choice for distributed systems
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Who triggered the optimization
    user_id VARCHAR(255) NOT NULL,

    -- The EC2 instance that is being rightsized
    instance_id VARCHAR(255) NOT NULL,

    -- Original and suggested instance types
    original_instance_type VARCHAR(100) NOT NULL,
    recommended_instance_type VARCHAR(100) NOT NULL,

    -- Estimated monthly savings – may be unknown until the recommendation is generated
    estimated_monthly_savings DECIMAL(10, 2),

    -- Current lifecycle state
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    -- Final outcome after the operation finishes
    outcome VARCHAR(50) NOT NULL DEFAULT 'pending',

    -- Human‑readable error message (used for Slack alerts, etc.)
    error_details TEXT,

    -- When the recommendation was actually applied
    applied_at TIMESTAMP WITH TIME ZONE,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- --------------------------------------------------------------
-- 3️⃣  Optional FK – uncomment if you have a users table
-- --------------------------------------------------------------
-- ALTER TABLE optimizations
--   ADD CONSTRAINT fk_optimizations_user
--   FOREIGN KEY (user_id) REFERENCES users(id);

-- --------------------------------------------------------------
-- 4️⃣  CHECK constraints – enforce allowed values
-- --------------------------------------------------------------
ALTER TABLE optimizations
  ADD CONSTRAINT chk_status
  CHECK (status IN ('pending', 'applying', 'completed', 'failed'));

ALTER TABLE optimizations
  ADD CONSTRAINT chk_outcome
  CHECK (outcome IN ('pending', 'success', 'failed', 'rolled_back'));

-- --------------------------------------------------------------
-- 5️⃣  Trigger to keep updated_at current
-- --------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_optimizations_updated_at
BEFORE UPDATE ON optimizations
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- --------------------------------------------------------------
-- 6️⃣  Indexes – the most common query patterns
-- --------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_opt_user_id
    ON optimizations(user_id);

CREATE INDEX IF NOT EXISTS idx_opt_instance_id
    ON optimizations(instance_id);

CREATE INDEX IF NOT EXISTS idx_opt_status
    ON optimizations(status);

CREATE INDEX IF NOT EXISTS idx_opt_created_at
    ON optimizations(created_at);

-- --------------------------------------------------------------
-- 7️⃣  Comments – documentation for future maintainers
-- --------------------------------------------------------------
COMMENT ON TABLE optimizations IS
  'Audit table for EC2 rightsizing optimization actions';

COMMENT ON COLUMN optimizations.id IS
  'Unique identifier for the optimization record';

COMMENT ON COLUMN optimizations.user_id IS
  'ID of the user who triggered the optimization';

COMMENT ON COLUMN optimizations.instance_id IS
  'AWS EC2 instance ID that was optimized';

COMMENT ON COLUMN optimizations.original_instance_type IS
  'Original EC2 instance type (e.g., t3.large)';

COMMENT ON COLUMN optimizations.recommended_instance_type IS
  'Recommended smaller instance type for rightsizing';

COMMENT ON COLUMN optimizations.estimated_monthly_savings IS
  'Estimated monthly cost savings in USD';

COMMENT ON COLUMN optimizations.status IS
  'Current status: pending, applying, completed, failed';

COMMENT ON COLUMN optimizations.outcome IS
  'Final outcome: success, failed, rolled_back';

COMMENT ON COLUMN optimizations.error_details IS
  'Error message details if the operation failed (used for Slack alerts)';

COMMENT ON COLUMN optimizations.applied_at IS
  'Timestamp when the new instance type was actually applied';

COMMENT ON COLUMN optimizations.created_at IS
  'Record creation timestamp';

COMMENT ON COLUMN optimizations.updated_at IS
  'Last update timestamp (auto‑updated by trigger)';

-- --------------------------------------------------------------
-- 8️⃣  End of migration
-- --------------------------------------------------------------