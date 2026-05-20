-- Test for session creation
INSERT INTO sessions (user_id, node_id) VALUES (1, 1);
SELECT * FROM sessions WHERE id = (SELECT MAX(id) FROM sessions);

-- Test for session update
UPDATE sessions SET end_timestamp = CURRENT_TIMESTAMP, status = 'completed' WHERE id = 1;
SELECT * FROM sessions WHERE id = 1;

-- Test for session retrieval by user_id
SELECT * FROM sessions WHERE user_id = 1;