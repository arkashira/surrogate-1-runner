-- Create requests table with SLA support
CREATE TABLE IF NOT EXISTS requests (
    id              TEXT PRIMARY KEY,
    request_type    TEXT NOT NULL DEFAULT 'default',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sla_days        INTEGER NOT NULL DEFAULT 5,
    due_at          TIMESTAMPTZ NOT NULL,
    status          TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'done', 'cancelled')),
    breached_at     TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}'::JSONB,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for SLA queries
CREATE INDEX IF NOT EXISTS idx_requests_due_at          ON requests (due_at);
CREATE INDEX IF NOT EXISTS idx_requests_status         ON requests (status);
CREATE INDEX IF NOT EXISTS idx_requests_request_type   ON requests (request_type);
CREATE INDEX IF NOT EXISTS idx_requests_breached_at    ON requests (breached_at) WHERE breached_at IS NOT NULL;

-- Function to compute business-day due date (skip weekends)
-- start_date: base date, business_days: number of business days to add
CREATE OR REPLACE FUNCTION business_day_due(start_date TIMESTAMPTZ, business_days INTEGER)
RETURNS TIMESTAMPTZ AS $$
DECLARE
    d DATE := start_date::DATE;
    added INTEGER := 0;
BEGIN
    WHILE added < business_days LOOP
        d := d + INTERVAL '1 day';
        -- skip Saturday (6) and Sunday (0)
        IF EXTRACT(ISODOW FROM d) < 6 THEN
            added := added + 1;
        END IF;
    END LOOP;
    -- preserve original time-of-day
    RETURN (d + (start_date::TIME)::INTERVAL) AT TIME ZONE 'UTC';
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Trigger: auto-calculate due_at on insert if not provided
CREATE OR REPLACE FUNCTION trg_set_request_due_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.due_at IS NULL THEN
        NEW.due_at := business_day_due(NEW.created_at, NEW.sla_days);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_request_due_at
    BEFORE INSERT ON requests
    FOR EACH ROW
    EXECUTE FUNCTION trg_set_request_due_at();

-- Trigger: auto-update breached_at when due_at passed and status not done
CREATE OR REPLACE FUNCTION trg_update_breach_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status <> 'done' AND NEW.due_at < NOW() AND NEW.breached_at IS NULL THEN
        NEW.breached_at := NOW();
    END IF;
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_breach_status
    BEFORE UPDATE ON requests
    FOR EACH ROW
    EXECUTE FUNCTION trg_update_breach_status();