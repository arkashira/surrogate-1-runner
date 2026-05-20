package config

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
)

// Config represents the application configuration
type Config struct {
	Port int `json:"port"`
}

// LoadConfig loads the application configuration from a file
func LoadConfig() (*Config, error) {
	// Load configuration from file
	data, err := ioutil.ReadFile("config.json")
	if err != nil {
		return nil, err
	}

	// Unmarshal JSON data
	var cfg Config
	err = json.Unmarshal(data, &cfg)
	if err != nil {
		return nil, err
	}

	return &cfg, nil
}

func main() {
	// Load configuration
	cfg, err := LoadConfig()
	if err != nil {
		log.Fatal(err)
	}

	// Print configuration
	log.Printf("Port: %d\n", cfg.Port)
}