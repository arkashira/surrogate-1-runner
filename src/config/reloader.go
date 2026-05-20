package config

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/fsnotify/fsnotify"
)

// Config represents the configuration for the surrogate-1 service
type Config struct {
	ServiceName    string   `json:"service_name"`
	InternalIP     string   `json:"internal_ip"`
	InternalPort   int      `json:"internal_port"`
	MatchCriteria  []string `json:"match_criteria"`
}

// Reloader watches for changes to the configuration file and reloads the configuration
type Reloader struct {
	configFile string
	config     *Config
	watcher    *fsnotify.Watcher
	mu         sync.RWMutex
}

// NewReloader returns a new Reloader instance
func NewReloader(configFile string) (*Reloader, error) {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return nil, err
	}

	reloader := &Reloader{
		configFile: configFile,
		watcher:    watcher,
	}

	if err := reloader.loadConfig(); err != nil {
		return nil, err
	}

	if err := reloader.watcher.Add(configFile); err != nil {
		return nil, err
	}

	go reloader.watchForChanges()

	return reloader, nil
}

// loadConfig loads the configuration from the file
func (r *Reloader) loadConfig() error {
	data, err := ioutil.ReadFile(r.configFile)
	if err != nil {
		return err
	}

	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		return err
	}

	r.mu.Lock()
	r.config = &config
	r.mu.Unlock()

	return nil
}

// watchForChanges watches for changes to the configuration file and reloads the configuration
func (r *Reloader) watchForChanges() {
	for {
		select {
		case event, ok := <-r.watcher.Events:
			if !ok {
				return
			}

			if event.Name == r.configFile && event.Op&fsnotify.Write == fsnotify.Write {
				if err := r.loadConfig(); err != nil {
					log.Printf("Error reloading configuration: %v", err)
				}
			}
		case err, ok := <-r.watcher.Errors:
			if !ok {
				return
			}

			log.Printf("Error watching configuration file: %v", err)
		}
	}
}

// GetConfig returns the current configuration
func (r *Reloader) GetConfig() *Config {
	r.mu.RLock()
	defer r.mu.RUnlock()

	return r.config
}

// ValidateConfig validates the configuration
func (r *Reloader) ValidateConfig() error {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if r.config == nil {
		return errors.New("configuration is nil")
	}

	if r.config.ServiceName == "" {
		return errors.New("service_name is required")
	}

	if r.config.InternalIP == "" {
		return errors.New("internal_ip is required")
	}

	if r.config.InternalPort == 0 {
		return errors.New("internal_port is required")
	}

	if len(r.config.MatchCriteria) == 0 {
		return errors.New("match_criteria is required")
	}

	return nil
}