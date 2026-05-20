package sdk

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"

	"gopkg.in/yaml.v2"
)

// Config represents the application configuration
type Config struct {
	RelayEndpoint   string            `yaml:"relay_endpoint"`
	JWTSecret       string            `yaml:"jwt_secret"`
	ChainRPCURLs    map[string]string `yaml:"chain_rpc_urls"`
}

// LoadConfig loads and validates the configuration from a YAML file
func LoadConfig(configPath string) (*Config, error) {
	// Check if config file exists
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("configuration file not found: %s", configPath)
	}

	// Read the config file
	data, err := ioutil.ReadFile(configPath)
	if err != nil {
		return nil, fmt.Errorf("failed to read configuration file: %v", err)
	}

	// Parse YAML
	var config Config
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, fmt.Errorf("failed to parse YAML configuration: %v", err)
	}

	// Validate required fields
	if config.RelayEndpoint == "" {
		log.Println("ERROR: Missing required field 'relay_endpoint'")
		return nil, fmt.Errorf("missing required field 'relay_endpoint'")
	}

	if config.JWTSecret == "" {
		log.Println("ERROR: Missing required field 'jwt_secret'")
		return nil, fmt.Errorf("missing required field 'jwt_secret'")
	}

	if config.ChainRPCURLs == nil {
		log.Println("ERROR: Missing required field 'chain_rpc_urls'")
		return nil, fmt.Errorf("missing required field 'chain_rpc_urls'")
	}

	// Validate chain RPC URLs is not empty
	if len(config.ChainRPCURLs) == 0 {
		log.Println("ERROR: 'chain_rpc_urls' cannot be empty")
		return nil, fmt.Errorf("'chain_rpc_urls' cannot be empty")
	}

	log.Println("Configuration loaded successfully")
	return &config, nil
}