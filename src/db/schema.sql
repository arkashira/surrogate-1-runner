-- User tier tracking
CREATE TABLE user_tiers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL UNIQUE REFERENCES users(id),
  tier VARCHAR(20) NOT NULL DEFAULT 'free',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  CONSTRAINT valid_tier CHECK (tier IN ('free', 'pro', 'enterprise'))
);

-- Track usage for enforcement
CREATE TABLE resource_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  resource_type VARCHAR(50) NOT NULL, -- 'dashboard' or 'alert'
  resource_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  CONSTRAINT valid_resource_type CHECK (resource_type IN ('dashboard', 'alert')),
  UNIQUE(user_id, resource_type, resource_id)
);

-- Index for efficient limit queries
CREATE INDEX idx_resource_usage_user ON resource_usage(user_id, resource_type);