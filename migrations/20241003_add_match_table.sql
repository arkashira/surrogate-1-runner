-- =========================================================
--  Create the `matches` table for provider‑investor matching
-- =========================================================

CREATE TABLE IF NOT EXISTS matches (
    id          SERIAL PRIMARY KEY,

    provider_id INTEGER NOT NULL
        REFERENCES providers(id) ON DELETE CASCADE,

    investor_id INTEGER NOT NULL
        REFERENCES investors(id) ON DELETE CASCADE,

    score       INTEGER NOT NULL
        CHECK (score >= 0 AND score <= 100),

    created_at  TIMESTAMP WITH TIME ZONE NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    -- Unique provider‑investor pair
    CONSTRAINT unique_provider_investor_pair
        UNIQUE (provider_id, investor_id)
);

-- Indexes for the most common queries
CREATE INDEX IF NOT EXISTS idx_matches_provider_id
    ON matches (provider_id);

CREATE INDEX IF NOT EXISTS idx_matches_investor_id
    ON matches (investor_id);

CREATE INDEX IF NOT EXISTS idx_matches_score
    ON matches (score);

CREATE INDEX IF NOT EXISTS idx_matches_created_at
    ON matches (created_at DESC);