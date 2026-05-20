CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY,
    term TEXT NOT NULL,
    definition TEXT NOT NULL,
    topic TEXT NOT NULL
);