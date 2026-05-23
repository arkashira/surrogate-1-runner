package test

import (
	"testing"
	"os"
	"path/filepath"
	"../parser"
)

func TestLargeInputParsing(t *testing.T) {
	// Load large test data
	data, err := os.ReadFile(filepath.Join("test", "fixtures", "large_data.json"))
	if err != nil {
		t.Fatalf("Failed to read test data: %v", err)
	}

	// Test parsing
	_, err = parser.Parse(data)
	if err != nil {
		t.Errorf("Failed to parse large input: %v", err)
	}

	// Add more specific assertions as needed
}