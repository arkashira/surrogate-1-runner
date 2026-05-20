package compliance

type Scanner struct {
	config *Config
}

func NewScanner(config *Config) *Scanner {
	return &Scanner{config: config}
}

func (s *Scanner) Scan() {
	// Implement scan logic here
	// Toggle rules based on config.RuleSets
}