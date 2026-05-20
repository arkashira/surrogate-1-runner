package config

import (
	"io/ioutil"
	"gopkg.in/yaml.v2"
	"log"
	"path/filepath"
)

type SurrogateConfig struct {
	Languages map[string]LanguageConfig `yaml:"languages"`
}

type LanguageConfig struct {
	Formatter string `yaml:"formatter"`
	Rules     string `yaml:"rules"`
}

func LoadConfig(configPath string) (*SurrogateConfig, error) {
	config := &SurrogateConfig{}

	configBytes, err := ioutil.ReadFile(filepath.Clean(configPath))
	if err != nil {
		return nil, err
	}

	err = yaml.Unmarshal(configBytes, config)
	if err != nil {
		return nil, err
	}

	return config, nil
}

func (c *SurrogateConfig) Validate() error {
	// Add validation logic here
	return nil
}