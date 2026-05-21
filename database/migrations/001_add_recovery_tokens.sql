-- Migration: Add recovery_tokens table for admin-generated user recovery tokens
-- Expires after 30 days, cryptographically secure, usage history logged

CREATE TABLE IF NOT EXISTS recovery_tokens (
    id BIGSERIAL PRIMARY KEY,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    user_id VARCHAR(255) NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,
    is_used BOOLEAN DEFAULT FALSE,
    ip_address VARCHAR(45),
    user_agent TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Index for looking up tokens by hash (for validation)
CREATE INDEX idx_recovery_tokens_token_hash ON recovery_tokens(token_hash);

-- Index for looking up tokens by user_id
CREATE INDEX idx_recovery_tokens_user_id ON recovery_tokens(user_id);

-- Index for finding active (non-expired, non-used) tokens
CREATE INDEX idx_recovery_tokens_active ON recovery_tokens(expires_at, is_used) WHERE is_used = FALSE;

-- Index for usage history queries
CREATE INDEX idx_recovery_tokens_created_at ON recovery_tokens(created_at DESC);