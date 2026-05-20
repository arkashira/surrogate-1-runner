package sdk

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v3"
)

// Config holds the relay configuration
type Config struct {
	RelayEndpoint string   `yaml:"relay_endpoint"`
	JWTSecret     string   `yaml:"jwt_secret"`
	ChainRPC      []string `yaml:"chain_rpc"`
}

// LoadConfig loads and validates the configuration from a YAML file
func LoadConfig(configPath string) (*Config, error) {
	// Check if config file exists
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("config file not found: %s", configPath)
	}

	// Read the config file
	data, err := ioutil.ReadFile(configPath)
	if err != nil {
		return nil, fmt.Errorf("failed to read config file: %v", err)
	}

	var cfg Config
	err = yaml.Unmarshal(data, &cfg)
	if err != nil {
		return nil, fmt.Errorf("failed to parse config: %v", err)
	}

	// Validate required fields
	if cfg.RelayEndpoint == "" {
		return nil, errors.New("relay_endpoint is required")
	}

	if cfg.JWTSecret == "" {
		return nil, errors.New("jwt_secret is required")
	}

	if len(cfg.ChainRPC) == 0 {
		return nil, errors.New("chain_rpc is required")
	}

	// Log validation results
	log.Printf("Config loaded successfully: %s", configPath)
	log.Printf("Relay endpoint: %s", cfg.RelayEndpoint)
	log.Printf("JWT secret: %s", cfg.JWTSecret)
	log.Printf("Chain RPC URLs: %v", cfg.ChainRPC)

	return &cfg, nil
}

// ValidateConfig checks if the config has all required fields
func ValidateConfig(cfg *Config) error {
	if cfg == nil {
		return errors.New("config is nil")
	}

	if cfg.RelayEndpoint == "" {
		return errors.New("relay_endpoint is missing")
	}

	if cfg.JWTSecret == "" {
		return errors.New("jwt_secret is missing")
	}

	if len(cfg.ChainRPC) == 0 {
		return errors.New("chain_rpc is missing")
	}

	return nil
}

// WriteConfig writes the config to a YAML file
func WriteConfig(cfg *Config, configPath string) error {
	data, err := yaml.Marshal(cfg)
	if err != nil {
		return fmt.Errorf("failed to marshal config: %v", err)
	}

	return ioutil.WriteFile(configPath, data, 0644)
}

// ValidateAndLog checks if the config is valid and logs errors if not
func ValidateAndLog(cfg *Config) error {
	if err := ValidateConfig(cfg); err != nil {
		log.Printf("Config validation error: %v", err)
		return err
	}

	return nil
}