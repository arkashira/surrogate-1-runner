-- Path: /opt/axentx/surrogate-1/backend/migrations/0042_add_playbook_table.sql

-- Create founders table for user reference
CREATE TABLE IF NOT EXISTS founders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create playbooks table with comprehensive schema
CREATE TABLE IF NOT EXISTS playbooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    founder_id UUID NOT NULL REFERENCES founders(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    word_count INTEGER NOT NULL CHECK (word_count <= 800),
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'failed')),
    email_sent BOOLEAN NOT NULL DEFAULT FALSE,
    email_sent_at TIMESTAMP WITH TIME ZONE,
    llama_gate_response_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT word_count_limit CHECK (word_count BETWEEN 0 AND 800)
);

-- Performance indexes
CREATE INDEX idx_playbooks_founder_id ON playbooks(founder_id);
CREATE INDEX idx_playbooks_generated_at ON playbooks(generated_at);
CREATE INDEX idx_playbooks_status ON playbooks(status);
CREATE INDEX idx_playbooks_email_sent_at ON playbooks(email_sent_at);

-- Documentation comments
COMMENT ON TABLE playbooks IS 'Weekly markdown playbooks generated from founder profile via Llama-Gate';
COMMENT ON COLUMN playbooks.title IS 'Human-readable playbook title';
COMMENT ON COLUMN playbooks.content IS 'Markdown-formatted playbook content (max 800 words)';
COMMENT ON COLUMN playbooks.word_count IS 'Actual word count of generated content';
COMMENT ON COLUMN playbooks.status IS 'Generation status: draft, published, or failed';
COMMENT ON COLUMN playbooks.email_sent IS 'Whether email notification was sent to founder';
COMMENT ON COLUMN playbooks.email_sent_at IS 'Timestamp when email was sent';
COMMENT ON COLUMN playbooks.llama_gate_response_id IS 'Reference to Llama-Gate API response for audit';