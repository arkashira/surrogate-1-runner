package multiplexer

import (
	"errors"
	"fmt"
	"net/url"
)

// ValidateConfig checks the syntactic correctness of a Config.
// It ensures that each service has a unique, non‑empty name, a non‑empty
// target, and that the target parses as a valid URL.
func ValidateConfig(cfg *Config) error {
	if cfg == nil {
		return errors.New("config is nil")
	}
	seen := make(map[string]struct{}, len(cfg.Services))
	for i, svc := range cfg.Services {
		if svc.Name == "" {
			return fmt.Errorf("service at index %d missing required field 'name'", i)
		}
		if _, exists := seen[svc.Name]; exists {
			return fmt.Errorf("duplicate service name detected: %s", svc.Name)
		}
		seen[svc.Name] = struct{}{}

		if svc.Target == "" {
			return fmt.Errorf("service %q missing required field 'target'", svc.Name)
		}
		if _, err := url.ParseRequestURI(svc.Target); err != nil {
			return fmt.Errorf("service %q has invalid target URL %q: %w", svc.Name, svc.Target, err)
		}
	}
	return nil
}