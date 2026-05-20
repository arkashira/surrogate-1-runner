-- Create credits table for storing user monthly and bulk credit balances

CREATE TABLE IF NOT EXISTS credits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    monthly_credits INTEGER NOT NULL DEFAULT 0,
    bulk_credits INTEGER NOT NULL DEFAULT 0,
    last_monthly_reset TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster user credit lookups
CREATE INDEX idx_credits_user_id ON credits(user_id);

-- Index for finding accounts needing monthly reset
CREATE INDEX idx_credits_last_monthly_reset ON credits(last_monthly_reset);

-- Comments for documentation
COMMENT ON TABLE credits IS 'Stores monthly and bulk credit balances per user';
COMMENT ON COLUMN credits.monthly_credits IS 'Monthly credits that reset periodically';
COMMENT ON COLUMN credits.bulk_credits IS 'Purchased bulk credits that do not expire';