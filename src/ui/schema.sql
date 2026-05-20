CREATE TABLE formatting_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repository TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_repository ON formatting_status(repository);