-- --------------------------------------------------------------
-- Purpose: Store cost attribution for each commit, with temporal
--          boundaries and full auditability.
-- --------------------------------------------------------------

BEGIN;

-----------------------------------------------------------------
-- 1. Table definition
-----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS commit_costs (
    id          BIGSERIAL PRIMARY KEY,
    commit_sha  VARCHAR(40) NOT NULL,          -- SHA‑1 hash (exact length)
    repo        VARCHAR(255) NOT NULL,
    branch      VARCHAR(255) NOT NULL,
    cost        NUMERIC(20,6) NOT NULL,        -- e.g. $12345.678901
    start_time  TIMESTAMPTZ NOT NULL,          -- when the cost period begins
    end_time    TIMESTAMPTZ NOT NULL,          -- when the cost period ends
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-----------------------------------------------------------------
-- 2. Constraints
-----------------------------------------------------------------
-- One record per commit SHA within a given repo/branch
ALTER TABLE commit_costs
    ADD CONSTRAINT uq_commit_repo_branch
        UNIQUE (commit_sha, repo, branch);

-----------------------------------------------------------------
-- 3. Indexes – tuned for the most common query patterns
-----------------------------------------------------------------
-- a) Fast lookup by repo + branch (often filtered together)
CREATE INDEX IF NOT EXISTS idx_commit_costs_repo_branch
    ON commit_costs (repo, branch);

-- b) Direct lookup by commit SHA (primary key alternative)
CREATE INDEX IF NOT EXISTS idx_commit_costs_sha
    ON commit_costs (commit_sha);

-- c) Time‑range queries (e.g., “costs incurred in the last week”)
CREATE INDEX IF NOT EXISTS idx_commit_costs_time
    ON commit_costs (start_time, end_time);

-- d) Composite covering index for the exact most‑common pattern:
--    repo + branch + commit_sha
CREATE INDEX IF NOT EXISTS idx_commit_costs_repo_branch_sha
    ON commit_costs (repo, branch, commit_sha);

-----------------------------------------------------------------
-- 4. Trigger to keep `updated_at` current
-----------------------------------------------------------------
CREATE OR REPLACE FUNCTION trg_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON commit_costs;
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON commit_costs
FOR EACH ROW EXECUTE FUNCTION trg_update_timestamp();

COMMIT;