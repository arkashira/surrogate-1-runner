package multiplexer

import (
	"os"

	"github.com/fsnotify/fsnotify"
	"gopkg.in/yaml.v3"
)

// ServiceConfig describes a single downstream service that the
// multiplexer can route to.
type ServiceConfig struct {
	// Name is a unique identifier for the service.
	Name string `yaml:"name"`
	// Target is the upstream URL (e.g. http://host:port) that receives
	// the proxied request.
	Target string `yaml:"target"`
	// Optional timeout in seconds; zero means use default.
	TimeoutSeconds int `yaml:"timeout_seconds,omitempty"`
}

// Config is the top‑level YAML structure.
type Config struct {
	Services []ServiceConfig `yaml:"services"`
}

// LoadConfig reads a YAML file from the given path, unmarshals it into a
// Config struct and validates the result.  It returns the parsed Config
// or an error if the file cannot be read, the YAML is malformed, or the
// validation fails.
func LoadConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, err
	}
	if err := ValidateConfig(&cfg); err != nil {
		return nil, err
	}
	return &cfg, nil
}

// WatchConfig watches the supplied file for changes (write/create events)
// and invokes onChange with a freshly loaded and validated Config.
// It returns an error if the file watcher cannot be created.
func WatchConfig(path string, onChange func(*Config)) error {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return err
	}
	// Ensure the watcher is closed when the caller stops the process.
	go func() {
		defer watcher.Close()
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				// React to writes or creates – typical when a config file is
				// overwritten atomically.
				if event.Op&(fsnotify.Write|fsnotify.Create) != 0 {
					if cfg, err := LoadConfig(path); err == nil {
						onChange(cfg)
					}
				}
			case _, ok := <-watcher.Errors:
				if !ok {
					return
				}
				// Errors are intentionally ignored here; the caller can
				// decide to log them via the onChange callback if needed.
			}
		}
	}()
	return watcher.Add(path)
}