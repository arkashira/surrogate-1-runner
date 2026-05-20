-- Migration to create the validation_projects table for the surrogate‑1 backend.
-- This table stores projects created via the "New Validation Project" UI flow.
-- It includes basic metadata, status tracking, timestamps, and integrity constraints.

BEGIN;

-- 1️⃣  Create the table
CREATE TABLE IF NOT EXISTS validation_projects (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- FK to users table – cascade delete keeps data clean
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Core project metadata – all limited to 100 chars
    name            TEXT NOT NULL CHECK (char_length(name) <= 100),
    description     TEXT NOT NULL CHECK (char_length(description) <= 100),
    target_market   TEXT NOT NULL CHECK (char_length(target_market) <= 100),

    -- Status – keep the set of allowed values explicit
    status          TEXT NOT NULL DEFAULT 'In-Progress'
                    CHECK (status IN ('In-Progress', 'Completed', 'Archived')),

    -- Timestamps – both default to the current instant
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2️⃣  Indexes for the most common queries
CREATE INDEX IF NOT EXISTS idx_validation_projects_user_id
    ON validation_projects (user_id);

CREATE INDEX IF NOT EXISTS idx_validation_projects_status
    ON validation_projects (status);

-- 3️⃣  Trigger to keep updated_at current
CREATE OR REPLACE FUNCTION update_validation_projects_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validation_projects_updated_at
BEFORE UPDATE ON validation_projects
FOR EACH ROW
EXECUTE FUNCTION update_validation_projects_updated_at();

COMMIT;