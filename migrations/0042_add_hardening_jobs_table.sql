CREATE TABLE hardening_jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL UNIQUE,
    vm_ids TEXT[] NOT NULL,
    policy_version VARCHAR(255) NOT NULL DEFAULT 'latest',
    status VARCHAR(20) NOT NULL DEFAULT 'queued',
    error_details TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);