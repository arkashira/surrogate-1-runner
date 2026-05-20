/*********************************************************************
 * 0044 – Job failure tracking
 *
 *  * job_failures          – one row per job execution that failed
 *  * job_failure_history  – many‑to‑many link between a failure and the
 *                           API request signatures that were involved
 *********************************************************************/

-- 1. Core failures table
CREATE TABLE job_failures (
    id          SERIAL PRIMARY KEY,
    job_id      INTEGER NOT NULL,
    status      VARCHAR(50) NOT NULL,               -- e.g. "failed", "timeout"
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. History linking failures to signatures
CREATE TABLE job_failure_history (
    id                         SERIAL PRIMARY KEY,
    job_failure_id            INTEGER NOT NULL,
    api_request_signature_id   INTEGER NOT NULL,
    status                     VARCHAR(50) NOT NULL,   -- status *at the time* of linking
    created_at                 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_failure_hist_failure
        FOREIGN KEY (job_failure_id)
        REFERENCES job_failures (id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_failure_hist_signature
        FOREIGN KEY (api_request_signature_id)
        REFERENCES api_request_signatures (id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- 3. Indexes for the two lookup directions
CREATE INDEX idx_failure_hist_failure_id
    ON job_failure_history (job_failure_id);
CREATE INDEX idx_failure_hist_signature_id
    ON job_failure_history (api_request_signature_id);