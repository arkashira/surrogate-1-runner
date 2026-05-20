package auth

import (
	"testing"
)

func TestGetStaticToken(t *testing.T) {
	token := GetStaticToken()
	if token == "" {
		t.Errorf("Expected non-empty token, got empty string")
	}
}

func TestGetMappings(t *testing.T) {
	mappings := GetMappings()
	if len(mappings.Mappings) != 0 {
		t.Errorf("Expected empty mappings, got %d", len(mappings.Mappings))
	}
}

func TestAddMapping(t *testing.T) {
	AddMapping("service1", 8080)
	if len(GetMappings().Mappings) != 1 {
		t.Errorf("Expected 1 mapping, got %d", len(GetMappings().Mappings))
	}
}

func TestDeleteMapping(t *testing.T) {
	DeleteMapping("service1")
	if len(GetMappings().Mappings) != 0 {
		t.Errorf("Expected 0 mappings, got %d", len(GetMappings().Mappings))
	}
}