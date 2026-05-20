-- Migration: Add model_metadata table for storing extracted metadata from model artifacts
-- Date: 2024-06-04
-- Author: axentx-dev-bot

-- Create model_metadata table for storing extracted metadata
CREATE TABLE IF NOT EXISTS model_metadata (
    id SERIAL PRIMARY KEY,
    model_id UUID NOT NULL,
    dataset_source TEXT,
    bias_metrics JSONB,
    extraction_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    extraction_status TEXT NOT NULL DEFAULT 'success',
    extraction_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Index for efficient lookups by model_id
    CONSTRAINT unique_model_metadata UNIQUE (model_id, extraction_timestamp)
);

-- Create index on model_id for fast joins with model artifacts
CREATE INDEX IF NOT EXISTS idx_model_metadata_model_id ON model_metadata(model_id);

-- Create index on extraction_timestamp for time-based queries
CREATE INDEX IF NOT EXISTS idx_model_metadata_extraction_timestamp ON model_metadata(extraction_timestamp);

-- Create index on extraction_status for filtering failed extractions
CREATE INDEX IF NOT EXISTS idx_model_metadata_extraction_status ON model_metadata(extraction_status);

-- Add comment to table for documentation
COMMENT ON TABLE model_metadata IS 'Stores extracted metadata from model artifacts including dataset source, bias metrics, and extraction status';

-- Add comment to bias_metrics column
COMMENT ON COLUMN model_metadata.bias_metrics IS 'JSONB field containing bias metrics extracted from model artifacts';

-- Add comment to extraction_status column
COMMENT ON COLUMN model_metadata.extraction_status IS 'Status of metadata extraction: success, partial, or failed';

-- Add comment to extraction_error column
COMMENT ON COLUMN model_metadata.extraction_error IS 'Error message if extraction failed or encountered malformed data';