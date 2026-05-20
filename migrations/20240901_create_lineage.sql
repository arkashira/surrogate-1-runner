-- Create table for storing lineage edges between datasets, jobs, and model versions
CREATE TABLE lineage_edges (
    id SERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL,
    source_type VARCHAR(50) NOT NULL CHECK (source_type IN ('dataset', 'job', 'model_version')),
    target_id BIGINT NOT NULL,
    target_type VARCHAR(50) NOT NULL CHECK (target_type IN ('dataset', 'job', 'model_version')),
    edge_type VARCHAR(50) NOT NULL CHECK (edge_type IN ('input', 'output', 'transformed_by')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (source_id) REFERENCES datasets(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES model_versions(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES datasets(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES model_versions(id) ON DELETE CASCADE
);

-- Add indexes for efficient graph traversal queries
CREATE INDEX idx_lineage_source ON lineage_edges (source_id, source_type, edge_type);
CREATE INDEX idx_lineage_target ON lineage_edges (target_id, target_type, edge_type);
CREATE INDEX idx_lineage_edge_type ON lineage_edges (edge_type);