package validate

// Config holds validation settings
type Config struct {
	EnableSecurityScan bool
	SeverityThreshold  string // e.g., "CRITICAL,HIGH"
	Tool               string // e.g., "trivy"
}

// DefaultConfig returns default validation configuration
func DefaultConfig() *Config {
	return &Config{
		EnableSecurityScan: true, // Enabled by default for safety
		SeverityThreshold:  "CRITICAL,HIGH",
		Tool:               "trivy",
	}
}