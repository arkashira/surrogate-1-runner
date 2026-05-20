package config

type SOC2Config struct {
    // SOC2 specific configuration fields
    SOC2Compliance bool `yaml:"soc2_compliance"`
    // Add other SOC2 specific fields as needed
}

func NewSOC2Config() *SOC2Config {
    return &SOC2Config{
        SOC2Compliance: false,
    }
}