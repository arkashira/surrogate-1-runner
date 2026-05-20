/*********************************************************************
 * 0043 – API request signatures
 *
 *  * api_request_signatures          – master list of distinct signatures
 *  * api_request_signature_history  – many‑to‑many link between a signature
 *                                     and a job execution, with status
 *
 *  All timestamps are stored in UTC (PostgreSQL’s TIMESTAMP WITHOUT TZ
 *  together with the server’s UTC configuration is the usual pattern).
 *********************************************************************/

-- 1. Master table – one row per distinct signature
CREATE TABLE api_request_signatures (
    id          SERIAL PRIMARY KEY,
    signature   VARCHAR(255) NOT NULL UNIQUE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. History table – records every time a signature is used by a job
CREATE TABLE api_request_signature_history (
    id                         SERIAL PRIMARY KEY,
    api_request_signature_id   INTEGER NOT NULL,
    job_id                     INTEGER NOT NULL,
    status                     VARCHAR(50) NOT NULL,
    created_at                 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sig_hist_signature
        FOREIGN KEY (api_request_signature_id)
        REFERENCES api_request_signatures (id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- 3. Indexes for the two most common lookup patterns
CREATE INDEX idx_sig_hist_signature_id
    ON api_request_signature_history (api_request_signature_id);
CREATE INDEX idx_sig_hist_job_id
    ON api_request_signature_history (job_id);