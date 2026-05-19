CREATE TABLE interactions (
    id              SERIAL PRIMARY KEY,
    provider_id     INTEGER NOT NULL,
    investor_id     INTEGER NOT NULL,
    timestamp       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    interaction_type VARCHAR(50) NOT NULL,
    CONSTRAINT fk_interactions_provider
        FOREIGN KEY (provider_id) REFERENCES providers(id),
    CONSTRAINT fk_interactions_investor
        FOREIGN KEY (investor_id) REFERENCES investors(id)
);