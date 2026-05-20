-- Migration: Add file_metadata table for storing ingested file metadata
-- Story: As a data engineer, I want each ingested file to have extracted metadata
--         so I can filter and search datasets.

-- Create the file_metadata table
CREATE TABLE IF NOT EXISTS file_metadata (
    file_id UUID PRIMARY KEY,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(255) NOT NULL,
    sha256_checksum VARCHAR(64) NOT NULL,
    ingestion_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add unique constraint on file_id (primary key already enforces this, but explicit for clarity)
-- Add unique constraint on sha256_checksum to prevent duplicate file content
ALTER TABLE file_metadata 
    ADD CONSTRAINT unique_sha256_checksum UNIQUE (sha256_checksum);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_file_metadata_ingestion_timestamp 
    ON file_metadata(ingestion_timestamp);

CREATE INDEX IF NOT EXISTS idx_file_metadata_mime_type 
    ON file_metadata(mime_type);

CREATE INDEX IF NOT EXISTS idx_file_metadata_file_size 
    ON file_metadata(file_size);

CREATE INDEX IF NOT EXISTS idx_file_metadata_sha256 
    ON file_metadata(sha256_checksum);

-- Function to update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to auto-update updated_at on row modification
CREATE TRIGGER update_file_metadata_updated_at
    BEFORE UPDATE ON file_metadata
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();