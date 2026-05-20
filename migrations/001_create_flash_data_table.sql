CREATE TABLE flash_data (
    id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL,
    duration_ms REAL NOT NULL
);