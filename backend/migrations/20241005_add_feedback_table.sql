-- Migration: Add feedback table for investor ratings on provider profiles
-- Created: 2024-10-05
-- Purpose: Store 1-5 star ratings and optional comments from investors to providers
--          after a 'Deal Closed' match. One feedback per investor-provider pair.

-- Create feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    investor_id INTEGER NOT NULL REFERENCES investors(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique constraint: one feedback per investor-provider pair
    CONSTRAINT uq_feedback_investor_provider UNIQUE (investor_id, provider_id)
);

-- Index for efficient queries on provider (displaying average rating on profile)
CREATE INDEX IF NOT EXISTS idx_feedback_provider_id ON feedback(provider_id);

-- Index for efficient queries on investor (viewing their given feedback)
CREATE INDEX IF NOT EXISTS idx_feedback_investor_id ON feedback(investor_id);

-- Index for computing average rating per provider
CREATE INDEX IF NOT EXISTS idx_feedback_rating_provider ON feedback(provider_id, rating);

-- Rollback migration (if needed)
-- DROP TABLE IF EXISTS feedback CASCADE;