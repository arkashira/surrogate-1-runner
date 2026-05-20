package config

import (
	"testing"
	"path/filepath"
)

func TestLoadConfig(t *testing.T) {
	configPath := filepath.Join("testdata", "valid_config.yml")
	config, err := LoadConfig(configPath)
	if err != nil {
		t.Fatalf("Failed to load config: %v", err)
	}

	if config == nil {
		t.Fatal("Config is nil")
	}

	if len(config.Languages) == 0 {
		t.Fatal("No languages in config")
	}
}

func TestInvalidConfig(t *testing.T) {
	configPath := filepath.Join("testdata", "invalid_config.yml")
	_, err := LoadConfig(configPath)
	if err == nil {
		t.Fatal("Expected error for invalid config")
	}
}