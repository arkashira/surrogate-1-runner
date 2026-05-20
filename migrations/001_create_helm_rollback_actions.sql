CREATE TABLE IF NOT EXISTS helm_rollback_actions (
	id              SERIAL PRIMARY KEY,
	release_name    TEXT NOT NULL,
	namespace       TEXT NOT NULL,
	target_revision INTEGER NOT NULL,
	attempted_at    TIMESTAMP NOT NULL,
	completed_at    TIMESTAMP,
	succeeded       BOOLEAN,
	error_message   TEXT
);