-- ------------------------------------------------------------
-- Run with: alembic upgrade head
-- ------------------------------------------------------------

CREATE TABLE cost_recommendations (
    id                     SERIAL PRIMARY KEY,
    resource_id            VARCHAR(255) NOT NULL,
    resource_type          VARCHAR(255) NOT NULL,
    recommendation_type   VARCHAR(255) NOT NULL,
    current_configuration  TEXT NOT NULL,
    recommended_configuration TEXT NOT NULL,
    estimated_savings      NUMERIC(12, 2) NOT NULL,   -- keep 2‑decimal precision
    actionable             BOOLEAN NOT NULL DEFAULT FALSE,
    created_at             TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Frequently‑used look‑ups
CREATE INDEX idx_cost_recommendations_resource
    ON cost_recommendations (resource_id, resource_type);

CREATE INDEX idx_cost_recommendations_actionable
    ON cost_recommendations (actionable);