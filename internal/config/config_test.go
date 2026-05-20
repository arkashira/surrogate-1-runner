package config

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/spf13/viper"
)

func TestLoadConfig(t *testing.T) {
	// Create a temporary config file
	tmpDir := t.TempDir()
	cfgPath := filepath.Join(tmpDir, "keep.yaml")
	content := []byte(`
rules:
  - protocol: tcp
    match_type: sni
    match_value: example.com
    target_ip: 10.0.0.1
    target_port: 443
`)
	if err := ioutil.WriteFile(cfgPath, content, 0o644); err != nil {
		t.Fatalf("write temp config: %v", err)
	}

	// Override default path
	configPath = cfgPath
	if err := LoadConfig(); err != nil {
		t.Fatalf("LoadConfig failed: %v", err)
	}

	cfg := GetConfig()
	if len(cfg.Rules) != 1 {
		t.Fatalf("expected 1 rule, got %d", len(cfg.Rules))
	}
	r := cfg.Rules[0]
	if r.Protocol != "tcp" || r.MatchType != "sni" || r.TargetIP != "10.0.0.1" || r.TargetPort != 443 {
		t.Fatalf("rule values not parsed correctly: %+v", r)
	}

	// Test hot reload
	newContent := []byte(`
rules:
  - protocol: tcp
    match_type: banner
    match_value: "HTTP/1.1"
    target_ip: 10.0.0.2
    target_port: 80
`)
	if err := ioutil.WriteFile(cfgPath, newContent, 0o644); err != nil {
		t.Fatalf("write new config: %v", err)
	}

	// Wait for debounce
	time.Sleep(12 * time.Second)

	cfg = GetConfig()
	if len(cfg.Rules) != 1 {
		t.Fatalf("expected 1 rule after reload, got %d", len(cfg.Rules))
	}
	r = cfg.Rules[0]
	if r.MatchType != "banner" || r.TargetIP != "10.0.0.2" || r.TargetPort != 80 {
		t.Fatalf("rule not reloaded correctly: %+v", r)
	}
}