CREATE TABLE IF NOT EXISTS startup_benchmark (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  market_size NUMERIC NOT NULL,
  team_experience NUMERIC NOT NULL,
  funding     NUMERIC NOT NULL,
  stage       TEXT NOT NULL,
  updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);