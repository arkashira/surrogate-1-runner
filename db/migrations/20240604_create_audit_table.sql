CREATE TABLE decision_audit (
    decision_id UUID PRIMARY KEY,
    policy_id UUID NOT NULL,
    policy_version INTEGER NOT NULL,
    context_hash VARCHAR(64) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    decision_output TEXT NOT NULL
);

CREATE INDEX idx_decision_audit_policy_id ON decision_audit(policy_id);
CREATE INDEX idx_decision_audit_timestamp ON decision_audit(timestamp);
CREATE INDEX idx_decision_audit_context_hash ON decision_audit(context_hash);