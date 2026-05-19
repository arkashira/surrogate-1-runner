package state

import (
	"os"
)

// Config holds configuration for the state persistence layer.
type Config struct {
	// Path is the filesystem path where the resourceVersion is persisted.
	Path string
}

// DefaultConfig returns a Config with a sensible default path.
// The path can be overridden by the SURROGATE_STATE_PATH environment variable.
func DefaultConfig() *Config {
	path := "/var/lib/surrogate-1/resource_version.json"
	if env := os.Getenv("SURROGATE_STATE_PATH"); env != "" {
		path = env
	}
	return &Config{Path: path}
}