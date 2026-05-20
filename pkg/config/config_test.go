package config

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestValidateConfig(t *testing.T) {
	config := map[string]interface{}{
		"service_mappings": []map[string]interface{}{
			{
				"protocol": "TCP",
				"port":     8080,
				"internal": "localhost:8081",
			},
		},
	}

	err := ValidateConfig(config)
	assert.NoError(t, err)
}

func TestValidateServiceMapping(t *testing.T) {
	mapping := ServiceMapping{
		Protocol: "TCP",
		Port:     8080,
		Internal: "localhost:8081",
	}

	err := ValidateServiceMapping(mapping)
	assert.NoError(t, err)
}