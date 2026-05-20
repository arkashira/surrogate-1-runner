-- Migration: create cost_forecasts table for 30‑day cost forecasting
-- This table stores daily generated cost forecasts. Each row represents
-- a forecast for a specific target date.

CREATE TABLE IF NOT EXISTS cost_forecasts (
    id                SERIAL PRIMARY KEY,
    generated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),  -- when the forecast was generated
    forecast_date     DATE        NOT NULL,                 -- the date being forecasted
    predicted_cost    NUMERIC(12, 2) NOT NULL,              -- predicted cost for the day
    actual_cost       NUMERIC(12, 2),                       -- actual cost (filled in later for comparison)
    created_by        VARCHAR(64) DEFAULT 'system',        -- audit: who/what generated the forecast
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now()    -- record creation timestamp
);

-- Index for common query pattern: look up forecasts by target date
CREATE INDEX IF NOT EXISTS idx_cost_forecasts_forecast_date
    ON cost_forecasts (forecast_date);

-- Index for querying forecasts by generation time
CREATE INDEX IF NOT EXISTS idx_cost_forecasts_generated_at
    ON cost_forecasts (generated_at);