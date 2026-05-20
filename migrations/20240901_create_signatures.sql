/* ------------------------------------------------------------------
   1️⃣  Create the signatures table
   ------------------------------------------------------------------ */
CREATE TABLE IF NOT EXISTS signatures (
    service        TEXT      NOT NULL,
    version        TEXT      NOT NULL,
    signature_hash BYTEA     NOT NULL,          -- encrypted hash
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (service, version)
);

-- Index that powers the 90‑day purge and any “created_at” scans
CREATE INDEX IF NOT EXISTS idx_signatures_created_at
    ON signatures (created_at);

/* ------------------------------------------------------------------
   2️⃣  Add descriptive comments
   ------------------------------------------------------------------ */
COMMENT ON TABLE signatures
    IS 'Store service‑version signatures for comparison and audit';

COMMENT ON COLUMN signatures.service
    IS 'Name of the service (e.g., “auth‑api”)';

COMMENT ON COLUMN signatures.version
    IS 'Semantic version of the service (e.g., “1.4.2”)';

COMMENT ON COLUMN signatures.signature_hash
    IS 'AES‑256 encrypted hash of the service signature';

COMMENT ON COLUMN signatures.created_at
    IS 'Timestamp when the signature was inserted';

/* ------------------------------------------------------------------
   3️⃣  Enable pgcrypto for encryption
   ------------------------------------------------------------------ */
CREATE EXTENSION IF NOT EXISTS pgcrypto;

/* ------------------------------------------------------------------
   4️⃣  Encrypt existing rows (if any) – idempotent
   ------------------------------------------------------------------ */
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pg_attribute
        WHERE attrelid = 'signatures'::regclass
          AND attname = 'signature_hash'
          AND atttypid = 'text'::regtype
    ) THEN
        ALTER TABLE signatures
            ALTER COLUMN signature_hash TYPE bytea
            USING encrypt(signature_hash::bytea, 'project_key', 'aes256');
    END IF;
END $$;

/* ------------------------------------------------------------------
   5️⃣  Retention policy – delete signatures older than 90 days
   ------------------------------------------------------------------ */
CREATE OR REPLACE FUNCTION purge_old_signatures()
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM signatures
    WHERE created_at < now() - INTERVAL '90 days';
END;
$$;

/* ------------------------------------------------------------------
   6️⃣  Schedule the purge with pg_cron (if available)
   ------------------------------------------------------------------ */
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_cron') THEN
        PERFORM cron.schedule(
            'daily_purge_signatures',
            '0 3 * * *',
            $$SELECT purge_old_signatures();$$
        );
    END IF;
END $$;

/* ------------------------------------------------------------------
   7️⃣  Fallback trigger – runs purge after any UPDATE/INSERT
   ------------------------------------------------------------------ */
CREATE OR REPLACE FUNCTION purge_old_signatures_trigger_fn()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM purge_old_signatures();
    RETURN NULL;
END;
$$;

-- The trigger only fires if pg_cron is NOT present
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_cron') THEN
        CREATE TRIGGER purge_old_signatures_trigger
            AFTER INSERT OR UPDATE ON signatures
            FOR EACH STATEMENT
            EXECUTE PROCEDURE purge_old_signatures_trigger_fn();
    END IF;
END $$;

/* ------------------------------------------------------------------
   8️⃣  REST endpoint – get baseline signature
   ------------------------------------------------------------------ */
-- Helper function that returns the signature as JSON
CREATE OR REPLACE FUNCTION get_baseline(
    _service TEXT,
    _version TEXT
)
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    sig JSON;
BEGIN
    SELECT json_agg(row_to_json(s))
      INTO sig
      FROM signatures s
     WHERE s.service = _service
       AND s.version = _version;

    RETURN sig;
END;
$$;

-- REST wrapper (PostgreSQL 15+ or extensions that expose REST)
CREATE OR REPLACE FUNCTION get_baseline_rest(
    _service TEXT,
    _version TEXT
)
RETURNS JSON
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN get_baseline(_service, _version);
END;
$$;

-- Expose the endpoint – adjust the syntax to match your REST extension
CREATE REST API get_baseline_rest
    METHOD = 'GET'
    PATH   = '/baseline/{service}/{version}'
    HANDLER = get_baseline_rest
    DESCRIPTION = 'Retrieve the baseline signature for a service/version';

-- Grant execution rights to the application role
GRANT EXECUTE ON FUNCTION get_baseline_rest(TEXT, TEXT) TO axentx_surrogate_1;