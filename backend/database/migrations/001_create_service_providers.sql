
CREATE TABLE service_providers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  service_type VARCHAR(50) NOT NULL,
  description TEXT NOT NULL,
  location VARCHAR(255) NOT NULL,
  website VARCHAR(500),
  phone VARCHAR(50),
  certifications TEXT[] DEFAULT '{}',
  years_of_experience INTEGER DEFAULT 0,
  hourly_rate DECIMAL(10, 2),
  tags TEXT[] DEFAULT '{}',
  rating DECIMAL(3, 2) DEFAULT 0,
  review_count INTEGER DEFAULT 0,
  status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'pending')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_service_providers_service_type ON service_providers(service_type);
CREATE INDEX idx_service_providers_location ON service_providers(location);
CREATE INDEX idx_service_providers_status ON service_providers(status);
CREATE INDEX idx_service_providers_search ON service_providers USING GIN(to_tsvector('english', name || ' ' || description || ' ' || COALESCE(tags::text, '')));