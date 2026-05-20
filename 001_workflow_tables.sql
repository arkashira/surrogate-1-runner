-- --------------------------------------------------------------
--  Workflows – the “current” version (mutable)
-- --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS workflows (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(255) NOT NULL,
    description   TEXT,
    inputs        JSONB NOT NULL DEFAULT '{}'::jsonb,
    steps         JSONB NOT NULL DEFAULT '[]'::jsonb,
    outputs       JSONB NOT NULL DEFAULT '{}'::jsonb,
    version       INTEGER NOT NULL DEFAULT 1,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_workflow_name_version UNIQUE (name, version)
);

CREATE INDEX IF NOT EXISTS idx_workflows_name        ON workflows(name);
CREATE INDEX IF NOT EXISTS idx_workflows_version     ON workflows(version);
CREATE INDEX IF NOT EXISTS idx_workflows_created_at ON workflows(created_at DESC);

-- --------------------------------------------------------------
--  Workflow Versions – immutable audit trail
-- --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS workflow_versions (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id   UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    version       INTEGER NOT NULL,
    name          VARCHAR(255) NOT NULL,
    description   TEXT,
    inputs        JSONB NOT NULL DEFAULT '{}'::jsonb,
    steps         JSONB NOT NULL DEFAULT '[]'::jsonb,
    outputs       JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_workflow_version UNIQUE (workflow_id, version)
);

CREATE INDEX IF NOT EXISTS idx_wv_workflow_id ON workflow_versions(workflow_id);
CREATE INDEX IF NOT EXISTS idx_wv_created_at  ON workflow_versions(created_at DESC);