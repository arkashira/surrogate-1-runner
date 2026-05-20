package config

type HIPAAConfig struct {
    // HIPAA specific configuration fields
    HIPAACompliance bool `yaml:"hipaa_compliance"`
    // Add other HIPAA specific fields as needed
}

func NewHIPAAConfig() *HIPAAConfig {
    return &HIPAAConfig{
        HIPAACompliance: false,
    }
}