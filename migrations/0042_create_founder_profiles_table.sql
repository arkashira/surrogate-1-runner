CREATE TABLE founder_profiles (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    stage VARCHAR(50),
    target_market VARCHAR(100),
    pricing_model VARCHAR(50),
    current_funnel VARCHAR(100),
    biggest_growth_pain TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_founder_profiles_email ON founder_profiles(email);