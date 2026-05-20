CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    start_timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_timestamp TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_node_id ON sessions(node_id);
CREATE INDEX IF NOT EXISTS idx_sessions_start_timestamp ON sessions(start_timestamp);

INSERT INTO sessions (user_id, node_id, start_timestamp)
VALUES (1, 1, CURRENT_TIMESTAMP)
RETURNING id;

UPDATE sessions
SET end_timestamp = CURRENT_TIMESTAMP, status = 'completed'
WHERE id = 1;

SELECT * FROM sessions WHERE user_id = 1;