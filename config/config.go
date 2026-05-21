package config

import (
	"os"
)

// Config holds the application configuration
type Config struct {
	TunnelEnabled bool
	TunnelURL     string
}

// LoadConfig loads configuration from environment variables
func LoadConfig() Config {
	return Config{
		TunnelEnabled: getEnvAsBool("TUNNEL_ENABLED", false),
		TunnelURL:     getEnv("TUNNEL_URL", "https://freedom-link.axentx.net"),
	}
}

func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}

func getEnvAsBool(name string, defaultValue bool) bool {
	valStr := getEnv(name, "")
	if valStr == "" {
		return defaultValue
	}
	return valStr != "0" && valStr != "false" && valStr != "False"
}