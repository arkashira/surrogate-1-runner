package state

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// Store is a thread‑safe persistence layer for the latest resourceVersion.
// It writes the value to a JSON file on disk and can recover from
// corrupted or missing files by returning an empty string.
type Store struct {
	mu   sync.Mutex
	path string
	// cached value to avoid repeated disk reads
	rv string
}

// NewStore creates a Store using the provided configuration.
func NewStore(cfg *Config) (*Store, error) {
	if cfg == nil {
		return nil, errors.New("config cannot be nil")
	}
	if cfg.Path == "" {
		return nil, errors.New("config.Path cannot be empty")
	}
	// Ensure directory exists
	dir := filepath.Dir(cfg.Path)
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return nil, fmt.Errorf("creating state dir: %w", err)
	}
	s := &Store{path: cfg.Path}
	// Load any existing value
	if err := s.load(); err != nil {
		// Log but do not fail; fallback to empty string
		// (logging omitted for brevity)
	}
	return s, nil
}

// Get returns the cached resourceVersion. If the store has not yet loaded
// a value, it will attempt to load from disk.
func (s *Store) Get() string {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.rv == "" {
		_ = s.load()
	}
	return s.rv
}

// Save persists the given resourceVersion to disk.
// It overwrites any existing value.
func (s *Store) Save(rv string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.rv = rv
	return s.write()
}

// load reads the JSON file and updates the cached value.
// It returns an error if the file cannot be read or parsed.
func (s *Store) load() error {
	data, err := os.ReadFile(s.path)
	if err != nil {
		// File missing is not fatal; treat as empty state.
		if os.IsNotExist(err) {
			s.rv = ""
			return nil
		}
		return fmt.Errorf("reading state file: %w", err)
	}
	var payload struct {
		ResourceVersion string `json:"resource_version"`
	}
	if err := json.Unmarshal(data, &payload); err != nil {
		return fmt.Errorf("parsing state file: %w", err)
	}
	s.rv = payload.ResourceVersion
	return nil
}

// write serialises the current value to the JSON file atomically.
func (s *Store) write() error {
	tmp := s.path + ".tmp"
	payload := struct {
		ResourceVersion string `json:"resource_version"`
	}{
		ResourceVersion: s.rv,
	}
	data, err := json.MarshalIndent(payload, "", "  ")
	if err != nil {
		return fmt.Errorf("marshalling state: %w", err)
	}
	if err := os.WriteFile(tmp, data, 0o644); err != nil {
		return fmt.Errorf("writing temp state file: %w", err)
	}
	// atomic rename
	if err := os.Rename(tmp, s.path); err != nil {
		return fmt.Errorf("renaming temp state file: %w", err)
	}
	return nil
}

// ExpiredError is returned when a stored resourceVersion is known to be
// expired (e.g., older than a configured TTL).  The caller can decide
// to fall back to a fresh watch.
type ExpiredError struct {
	Reason string
}

func (e *ExpiredError) Error() string {
	return fmt.Sprintf("resourceVersion expired: %s", e.Reason)
}

// IsExpired reports whether the error is an ExpiredError.
func IsExpired(err error) bool {
	var e *ExpiredError
	return errors.As(err, &e)
}

// Validate checks whether the stored resourceVersion is still usable.
// For this simplified implementation we consider a version expired if
// it is older than a configured TTL.  The TTL can be overridden by
// the SURROGATE_RV_TTL environment variable (seconds).
func (s *Store) Validate() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.rv == "" {
		return nil // nothing to validate
	}
	// In a real system we would parse the version timestamp.
	// Here we simply check if the file is older than TTL.
	info, err := os.Stat(s.path)
	if err != nil {
		return err
	}
	ttl := 60 * 60 * 24 // 24h default
	if env := os.Getenv("SURROGATE_RV_TTL"); env != "" {
		if v, err := time.ParseDuration(env + "s"); err == nil {
			ttl = int(v.Seconds())
		}
	}
	if time.Since(info.ModTime()) > time.Duration(ttl)*time.Second {
		return &ExpiredError{Reason: "file older than TTL"}
	}
	return nil
}