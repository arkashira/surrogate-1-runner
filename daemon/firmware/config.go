package firmware

import (
	"encoding/json"
	"errors"
	"fmt"
)

// Config represents the firmware configuration
type Config struct {
	GPUCount int `json:"gpu_count"`
}

// Validate checks if the configuration is valid
func (c *Config) Validate() error {
	if c.GPUCount < 1 {
		return errors.New("gpu count must be at least 1")
	}
	return nil
}

// LoadConfig loads the configuration from a JSON file
func LoadConfig(path string) (*Config, error) {
	var config Config
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	err = json.Unmarshal(data, &config)
	if err != nil {
		return nil, err
	}
	return &config, config.Validate()
}