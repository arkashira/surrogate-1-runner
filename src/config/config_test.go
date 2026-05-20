package config

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"testing"
)

func TestNewReloader(t *testing.T) {
	tmpFile, err := ioutil.TempFile("", "config")
	if err != nil {
		t.Fatal(err)
	}

	defer os.Remove(tmpFile.Name())

	config := Config{
		ServiceName:    "test-service",
		InternalIP:     "127.0.0.1",
		InternalPort:   8080,
		MatchCriteria:  []string{"test-criteria"},
	}

	data, err := json.Marshal(config)
	if err != nil {
		t.Fatal(err)
	}

	if _, err := tmpFile.Write(data); err != nil {
		t.Fatal(err)
	}

	if err := tmpFile.Close(); err != nil {
		t.Fatal(err)
	}

	reloader, err := NewReloader(tmpFile.Name())
	if err != nil {
		t.Fatal(err)
	}

	if reloader.config == nil {
		t.Fatal("configuration is nil")
	}

	if reloader.config.ServiceName != config.ServiceName {
		t.Errorf("expected service_name %q, got %q", config.ServiceName, reloader.config.ServiceName)
	}

	if reloader.config.InternalIP != config.InternalIP {
		t.Errorf("expected internal_ip %q, got %q", config.InternalIP, reloader.config.InternalIP)
	}

	if reloader.config.InternalPort != config.InternalPort {
		t.Errorf("expected internal_port %d, got %d", config.InternalPort, reloader.config.InternalPort)
	}

	if len(reloader.config.MatchCriteria) != len(config.MatchCriteria) {
		t.Errorf("expected match_criteria length %d, got %d", len(config.MatchCriteria), len(reloader.config.MatchCriteria))
	}

	for i, criteria := range config.MatchCriteria {
		if reloader.config.MatchCriteria[i] != criteria {
			t.Errorf("expected match_criteria %q, got %q", criteria, reloader.config.MatchCriteria[i])
		}
	}
}

func TestValidateConfig(t *testing.T) {
	reloader, err := NewReloader("/dev/null")
	if err != nil {
		t.Fatal(err)
	}

	reloader.mu.Lock()
	reloader.config = &Config{}
	reloader.mu.Unlock()

	if err := reloader.ValidateConfig(); err == nil {
		t.Fatal("expected error, got nil")
	}

	reloader.mu.Lock()
	reloader.config = &Config{
		ServiceName:    "test-service",
		InternalIP:     "127.0.0.1",
		InternalPort:   8080,
		MatchCriteria:  []string{"test-criteria"},
	}
	reloader.mu.Unlock()

	if err := reloader.ValidateConfig(); err != nil {
		t.Errorf("expected no error, got %v", err)
	}
}