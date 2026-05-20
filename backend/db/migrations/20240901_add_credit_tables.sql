-- File: /opt/axentx/surrogate-1/backend/db/migrations/20240901_add_credit_tables.sql
-- -------------------------------------------------------------------------------
-- Purpose:  Create the `account_credit` table that stores both monthly and bulk
--           credit balances, together with audit timestamps, indexes and an
--           automatic “updated_at” trigger.
-- -------------------------------------------------------------------------------

BEGIN;

--------------------------------------------------------------------
-- 1. Table definition
--------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS account_credit (
    account_id      UUID    NOT NULL PRIMARY KEY,               -- immutable identifier
    monthly_total  BIGINT  NOT NULL DEFAULT 0,                  -- quota granted each month
    monthly_used   BIGINT  NOT NULL DEFAULT 0,                  -- amount already consumed
    bulk_total     BIGINT  NOT NULL DEFAULT 0,                  -- one‑off or rollover pool
    bulk_used      BIGINT  NOT NULL DEFAULT 0,                  -- amount already consumed
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),        -- row creation time
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()         -- last modification time
);

--------------------------------------------------------------------
-- 2. Indexes – keep look‑ups and row‑level locking fast
--------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_account_credit_monthly_used
    ON account_credit (account_id, monthly_used);

CREATE INDEX IF NOT EXISTS idx_account_credit_bulk_used
    ON account_credit (account_id, bulk_used);

--------------------------------------------------------------------
-- 3. Trigger – keep `updated_at` in sync automatically
--------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_account_credit_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_account_credit_timestamp ON account_credit;

CREATE TRIGGER trg_update_account_credit_timestamp
BEFORE UPDATE ON account_credit
FOR EACH ROW
EXECUTE FUNCTION update_account_credit_timestamp();

COMMIT;