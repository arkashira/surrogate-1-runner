package compliance

type Config struct {
	HIPAARules  bool `yaml:"hipaa_rules"`
	SOC2Rules   bool `yaml:"soc2_rules"`
	RuleSets    map[string]bool `yaml:"rule_sets"`
}

func NewConfig() *Config {
	return &Config{
		RuleSets: make(map[string]bool),
	}
}