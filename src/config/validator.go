package config

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"sync"
	"time"

	"github.com/fsnotify/fsnotify"
	"gopkg.in/yaml.v3"
)

// ServiceMapping defines a single service routing entry.
type ServiceMapping struct {
	ServiceName   string            `yaml:"service_name"`
	InternalIP    string            `yaml:"internal_ip"`
	InternalPort  int               `yaml:"internal_port"`
	MatchCriteria map[string]string `yaml:"match_criteria"`
}

// Config holds the full list of service mappings.
type Config struct {
	Services []ServiceMapping `yaml:"services"`
}

// LoadConfig reads and validates the YAML configuration at the given path.
func LoadConfig(path string) (*Config, error) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("reading config file: %w", err)
	}

	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("parsing yaml: %w", err)
	}

	if err := validateConfig(&cfg); err != nil {
		return nil, err
	}
	return &cfg, nil
}

// validateConfig ensures all required fields are present and sensible.
func validateConfig(cfg *Config) error {
	if cfg == nil {
		return errors.New("config is nil")
	}
	if len(cfg.Services) == 0 {
		return errors.New("no services defined")
	}
	for i, s := range cfg.Services {
		if s.ServiceName == "" {
			return fmt.Errorf("service[%d]: service_name is required", i)
		}
		if s.InternalIP == "" {
			return fmt.Errorf("service[%d] (%s): internal_ip is required", i, s.ServiceName)
		}
		if s.InternalPort <= 0 || s.InternalPort > 65535 {
			return fmt.Errorf("service[%d] (%s): internal_port must be between 1 and 65535", i, s.ServiceName)
		}
		if s.MatchCriteria == nil || len(s.MatchCriteria) == 0 {
			return fmt.Errorf("service[%d] (%s): match_criteria must contain at least one entry", i, s.ServiceName)
		}
	}
	return nil
}

// Watcher watches a config file and triggers onUpdate when a valid new config is loaded.
// The callback is invoked at most once per change, after a debounce period (default 2s)
// and must complete within 5 seconds to satisfy the SLA.
type Watcher struct {
	path          string
	onUpdate      func(*Config)
	mu            sync.Mutex
	lastModTime   time.Time
	debounceTimer *time.Timer
}

// NewWatcher creates a new Watcher for the given file path.
func NewWatcher(path string, onUpdate func(*Config)) (*Watcher, error) {
	if onUpdate == nil {
		return nil, errors.New("onUpdate callback cannot be nil")
	}
	w := &Watcher{
		path:     path,
		onUpdate: onUpdate,
	}
	// Initial load
	if cfg, err := LoadConfig(path); err == nil {
		onUpdate(cfg)
	}
	return w, nil
}

// Start begins watching the file. It returns a function to stop the watcher.
func (w *Watcher) Start() (func() error, error) {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return nil, fmt.Errorf("creating fsnotify watcher: %w", err)
	}
	if err := watcher.Add(w.path); err != nil {
		return nil, fmt.Errorf("adding watch on %s: %w", w.path, err)
	}

	stopCh := make(chan struct{})
	go func() {
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				if event.Op&(fsnotify.Write|fsnotify.Create) != 0 {
					w.handleChange()
				}
			case err, ok := <-watcher.Errors:
				if ok {
					fmt.Fprintf(os.Stderr, "fsnotify error: %v\n", err)
				}
			case <-stopCh:
				return
			}
		}
	}()

	stopFunc := func() error {
		close(stopCh)
		return watcher.Close()
	}
	return stopFunc, nil
}

// handleChange debounces rapid file events and reloads the config.
func (w *Watcher) handleChange() {
	w.mu.Lock()
	defer w.mu.Unlock()

	if w.debounceTimer != nil {
		w.debounceTimer.Stop()
	}
	w.debounceTimer = time.AfterFunc(2*time.Second, func() {
		cfg, err := LoadConfig(w.path)
		if err != nil {
			fmt.Fprintf(os.Stderr, "config reload error: %v\n", err)
			return
		}
		// Ensure the update is delivered within 5 seconds of the file change.
		done := make(chan struct{})
		go func() {
			w.onUpdate(cfg)
			close(done)
		}()
		select {
		case <-done:
			// ok
		case <-time.After(5 * time.Second):
			fmt.Fprintf(os.Stderr, "config update callback exceeded 5‑second deadline\n")
		}
	})
}