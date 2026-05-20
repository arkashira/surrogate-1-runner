CREATE TABLE lab_configurations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    configuration TEXT NOT NULL
);

CREATE TABLE lab_configuration_versions (
    id SERIAL PRIMARY KEY,
    lab_configuration_id INTEGER NOT NULL REFERENCES lab_configurations(id),
    version INTEGER NOT NULL,
    configuration TEXT NOT NULL
);

CREATE TABLE community_ratings (
    id SERIAL PRIMARY KEY,
    lab_configuration_id INTEGER NOT NULL REFERENCES lab_configurations(id),
    rating INTEGER NOT NULL,
    comment TEXT
);