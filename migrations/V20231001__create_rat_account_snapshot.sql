
CREATE TABLE rat_account_snapshot (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    snapshot_date DATE NOT NULL,
    transaction_data JSONB NOT NULL,
    balance_data JSONB NOT NULL,
    UNIQUE (account_id, snapshot_date)
);