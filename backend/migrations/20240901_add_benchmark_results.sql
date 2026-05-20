-- Migration: create benchmark_results table for daily FPS benchmark ingestion

-- Create the table with required columns
CREATE TABLE IF NOT EXISTS benchmark_results (
    id SERIAL PRIMARY KEY,
    gpu TEXT NOT NULL,
    cpu TEXT NOT NULL,
    ram_gb INTEGER NOT NULL,
    fps DOUBLE PRECISION NOT NULL,
    "date" DATE NOT NULL
);

-- Index to speed up queries filtered by date
CREATE INDEX IF NOT EXISTS idx_benchmark_results_date ON benchmark_results ("date");