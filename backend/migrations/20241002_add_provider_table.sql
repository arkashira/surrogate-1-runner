CREATE TABLE IF NOT EXISTS providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pitch_id VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    tagline VARCHAR(500) NOT NULL,
    market VARCHAR(255) NOT NULL,
    traction_metrics JSONB NOT NULL,
    funding_stage VARCHAR(50) NOT NULL CHECK (funding_stage IN (
        'pre-seed',
        'seed',
        'series-a',
        'series-b',
        'series-c',
        'growth'
    )),
    executive_summary TEXT NOT NULL,
    deck_file_path VARCHAR(500),
    deck_file_size_bytes INTEGER,
    deck_content_type VARCHAR(100),
    contact_email VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN (
        'pending',
        'submitted',
        'under_review',
        'approved',
        'rejected'
    )),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_providers_pitch_id ON providers(pitch_id);
CREATE INDEX idx_providers_status ON providers(status);
CREATE INDEX idx_providers_email ON providers(contact_email);