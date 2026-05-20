package config

import (
	"fmt"
	"log"

	"github.com/BurntSushi/toml"
)

func GetPrivateKeyPath() string {
	// Load config from file
	data, err := ioutil.ReadFile("config.toml")
	if err != nil {
		log.Fatal(err)
	}

	// Parse config from TOML
	var config struct {
		PrivateKeyPath string `toml:"private_key_path"`
	}

	if _, err := toml.Decode(string(data), &config); err != nil {
		log.Fatal(err)
	}

	return config.PrivateKeyPath
}