CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    download_time TIMESTAMP NOT NULL,
    video_title TEXT NOT NULL,
    video_id TEXT NOT NULL,
    video_author TEXT NOT NULL,
    video_duration INTERVAL NOT NULL
);

CREATE INDEX idx_audit_logs_download_time ON audit_logs(download_time);
CREATE INDEX idx_audit_logs_video_id ON audit_logs(video_id);