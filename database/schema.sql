-- Ensure the sandbox table exists with updated schema
CREATE TABLE IF NOT EXISTS sandbox (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- New spend tracking columns
    spend_limit BIGINT NOT NULL DEFAULT 0,
    spend_used BIGINT NOT NULL DEFAULT 0,
    notify_threshold BIGINT NOT NULL DEFAULT 0,
    last_notified_at TIMESTAMP NULL
);