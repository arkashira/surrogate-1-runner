   CREATE TABLE alert_configs (
       project_id VARCHAR PRIMARY KEY,
       budget_limit DECIMAL,
       webhook_urls JSONB
   );