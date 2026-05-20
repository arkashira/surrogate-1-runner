CREATE TABLE feedback (
  id SERIAL PRIMARY KEY,
  recommendation_id INTEGER REFERENCES recommendations(id),
  user_id INTEGER REFERENCES users(id),
  feedback_text TEXT NOT NULL,
  feedback_time TIMESTAMP DEFAULT NOW()
);

CREATE TABLE aggregated_feedback (
  recommendation_id INTEGER REFERENCES recommendations(id),
  positive_feedback INTEGER DEFAULT 0,
  negative_feedback INTEGER DEFAULT 0,
  total_feedback INTEGER DEFAULT 0
);