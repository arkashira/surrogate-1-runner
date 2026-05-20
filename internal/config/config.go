package config

import (
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
)

// Rule represents a single routing rule loaded from the YAML file.
type Rule struct {
	Protocol   string `mapstructure:"protocol"`
	MatchType  string `mapstructure:"match_type"`
	MatchValue string `mapstructure:"match_value"`
	TargetIP   string `mapstructure:"target_ip"`
	TargetPort int    `mapstructure:"target_port"`
}

// Config holds all routing rules.
type Config struct {
	Rules []Rule `mapstructure:"rules"`
}

var (
	once       sync.Once
	instance   *Config
	mu         sync.RWMutex
	v          *viper.Viper
	configPath = "/opt/axentx/surrogate-1/config/keep.yaml"
)

// LoadConfig initializes the Viper instance, loads the YAML file, and sets up
// hot‑reload with a 10‑second debounce. It is safe to call multiple times.
func LoadConfig() error {
	var err error
	once.Do(func() {
		v = viper.New()
		// Ensure the directory exists; create if missing.
		if err = os.MkdirAll(filepath.Dir(configPath), 0o755); err != nil {
			logrus.WithError(err).Error("failed to create config directory")
			return
		}

		v.SetConfigFile(configPath)
		v.SetConfigType("yaml")

		// Initial load
		if err = loadIntoInstance(); err != nil {
			logrus.WithError(err).Error("initial config load failed")
			// Continue with empty config
		}

		// Watch for changes with a 10s debounce
		v.WatchConfig()
		v.OnConfigChange(func(e fsnotify.Event) {
			// Debounce rapid changes
			time.Sleep(10 * time.Second)
			if err := loadIntoInstance(); err != nil {
				logrus.WithError(err).Error("config reload failed, keeping previous config")
			} else {
				logrus.Info("config reloaded successfully")
			}
		})
	})
	return err
}

// loadIntoInstance unmarshals the current Viper config into the singleton instance.
// It returns an error if unmarshalling fails.
func loadIntoInstance() error {
	var cfg Config
	if err := v.Unmarshal(&cfg); err != nil {
		return err
	}
	mu.Lock()
	defer mu.Unlock()
	instance = &cfg
	return nil
}

// GetConfig returns the current configuration. It is safe for concurrent use.
func GetConfig() *Config {
	mu.RLock()
	defer mu.RUnlock()
	if instance == nil {
		return &Config{}
	}
	return instance
}