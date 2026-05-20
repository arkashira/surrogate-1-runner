-- This migration creates the table used to persist Roth wizard state.
-- Run with knex migrate:latest

CREATE TABLE IF NOT EXISTS roth_wizard_states (
  id UUID PRIMARY KEY,
  client_id TEXT NOT NULL,
  state_data JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Optional: index for quick lookup by client_id
CREATE INDEX IF NOT EXISTS idx_roth_wizard_states_client_id ON roth_wizard_states(client_id);