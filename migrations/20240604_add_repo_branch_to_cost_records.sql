/*=====================================================================
  Migration: 20240604_add_repo_branch_to_cost_records
  Location:  /opt/axentx/surrogate-1/migrations/
  Purpose:   Track the source repository and branch for each cost record.
  Features:  • Idempotent column addition
             • Indexes for fast look‑ups
             • All statements run inside a single transaction
=====================================================================*/

BEGIN;

--------------------------------------------------------------------
-- 1️⃣  Add columns if they are missing
--------------------------------------------------------------------
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'cost_records'
          AND column_name = 'repo_name'
    ) THEN
        ALTER TABLE cost_records
            ADD COLUMN repo_name TEXT;
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'cost_records'
          AND column_name = 'branch'
    ) THEN
        ALTER TABLE cost_records
            ADD COLUMN branch TEXT;
    END IF;
END$$;

--------------------------------------------------------------------
-- 2️⃣  Create indexes (only if they do not already exist)
--------------------------------------------------------------------
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_cost_records_repo_name'
          AND n.nspname = current_schema()
    ) THEN
        CREATE INDEX idx_cost_records_repo_name
            ON cost_records (repo_name);
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_cost_records_branch'
          AND n.nspname = current_schema()
    ) THEN
        CREATE INDEX idx_cost_records_branch
            ON cost_records (branch);
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_cost_records_repo_branch'
          AND n.nspname = current_schema()
    ) THEN
        CREATE INDEX idx_cost_records_repo_branch
            ON cost_records (repo_name, branch);
    END IF;
END$$;

COMMIT;