package config

import (
	"encoding/json"
	"io"
	"os"
	"strconv"
	"strings"
	"time"
)

// ---------------------------------------------------------------------
// Public structs
// ---------------------------------------------------------------------

// RedisConfig holds everything needed to create a go‑redis client.
type RedisConfig struct {
	Addr         string        // host:port
	Password     string        // optional password
	DB           int           // Redis DB number
	DialTimeout  time.Duration // connection timeout
	ReadTimeout  time.Duration // read timeout
	WriteTimeout time.Duration // write timeout
}

// AppConfig is the top‑level configuration object.  At the moment it only
// contains Redis settings, but it can be expanded later without breaking
// the API.
type AppConfig struct {
	Redis RedisConfig `json:"redis"`
}

// ---------------------------------------------------------------------
// Loading helpers
// ---------------------------------------------------------------------

// LoadFromEnv builds an AppConfig from environment variables.  All
// variables are optional – sensible defaults are supplied.
func LoadFromEnv() *AppConfig {
	rc := RedisConfig{
		Addr:         getEnv("REDIS_ADDR", "localhost:6379"),
		Password:     os.Getenv("REDIS_PASSWORD"), // empty string = no password
		DB:           getEnvInt("REDIS_DB", 0),
		DialTimeout:  getEnvDuration("REDIS_DIAL_TIMEOUT", 5*time.Second),
		ReadTimeout:  getEnvDuration("REDIS_READ_TIMEOUT", 3*time.Second),
		WriteTimeout: getEnvDuration("REDIS_WRITE_TIMEOUT", 3*time.Second),
	}
	return &AppConfig{Redis: rc}
}

// LoadFromFile reads a JSON file (e.g. /etc/surrogate/config.json) and
// unmarshals it into an AppConfig.  If the file cannot be read the
// function returns an error – callers can decide whether to fall back
// to env‑based defaults.
func LoadFromFile(path string) (*AppConfig, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	var cfg AppConfig
	dec := json.NewDecoder(io.LimitReader(f, 1<<20)) // 1 MiB limit
	if err := dec.Decode(&cfg); err != nil {
		return nil, err
	}
	return &cfg, nil
}

// DefaultConfig returns a fully populated config that works out of the
// box for local development.
func DefaultConfig() *AppConfig {
	return &AppConfig{
		Redis: RedisConfig{
			Addr:         "localhost:6379",
			Password:     "",
			DB:           0,
			DialTimeout:  5 * time.Second,
			ReadTimeout:  3 * time.Second,
			WriteTimeout: 3 * time.Second,
		},
	}
}

// ---------------------------------------------------------------------
// Internal helpers (env parsing)
// ---------------------------------------------------------------------

func getEnv(key, def string) string {
	if v := strings.TrimSpace(os.Getenv(key)); v != "" {
		return v
	}
	return def
}

func getEnvInt(key string, def int) int {
	if v := strings.TrimSpace(os.Getenv(key)); v != "" {
		if i, err := strconv.Atoi(v); err == nil {
			return i
		}
	}
	return def
}

func getEnvDuration(key string, def time.Duration) time.Duration {
	if v := strings.TrimSpace(os.Getenv(key)); v != "" {
		if d, err := time.ParseDuration(v); err == nil {
			return d
		}
	}
	return def
}