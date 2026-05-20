package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

const (
	defaultImage = "nginx:latest"
)

var defaultResources = map[string]map[string]string{
	"limits":   {"cpu": "500m", "memory": "256Mi"},
	"requests": {"cpu": "250m", "memory": "128Mi"},
}

var defaultEnv = map[string]string{
	"name":  "ENV",
	"value": "production",
}

type Container struct {
	Image     string                 `yaml:"image,omitempty"`
	Resources map[string]map[string]string `yaml:"resources,omitempty"`
	Env       []map[string]string    `yaml:"env,omitempty"`
}

type PodSpec struct {
	Containers []Container `yaml:"containers"`
}

type PodTemplateSpec struct {
	Spec PodSpec `yaml:"spec"`
}

type PodSpecWrapper struct {
	Spec PodTemplateSpec `yaml:"spec"`
}

func ensureContainerDefaults(c *Container) {
	if c.Image == "" {
		c.Image = defaultImage
	}

	if c.Resources == nil {
		c.Resources = make(map[string]map[string]string)
	}
	for key, val := range defaultResources {
		if c.Resources[key] == nil {
			c.Resources[key] = make(map[string]string)
		}
		for k, v := range val {
			c.Resources[key][k] = v
		}
	}

	if c.Env == nil {
		c.Env = []map[string]string{}
	}
	found := false
	for _, env := range c.Env {
		if env["name"] == defaultEnv["name"] {
			found = true
			break
		}
	}
	if !found {
		c.Env = append(c.Env, defaultEnv)
	}
}

func applyFixes(manifest *PodSpecWrapper) {
	for i := range manifest.Spec.Spec.Containers {
		ensureContainerDefaults(&manifest.Spec.Spec.Containers[i])
	}
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run config_fixer.go <path-to-manifest.yaml>")
		os.Exit(1)
	}

	path := os.Args[1]
	data, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatalf("Failed to read file: %v", err)
	}

	var manifest PodSpecWrapper
	err = yaml.Unmarshal(data, &manifest)
	if err != nil {
		log.Fatalf("Failed to unmarshal YAML: %v", err)
	}

	applyFixes(&manifest)

	data, err = yaml.Marshal(&manifest)
	if err != nil {
		log.Fatalf("Failed to marshal YAML: %v", err)
	}

	err = ioutil.WriteFile(path, data, 0644)
	if err != nil {
		log.Fatalf("Failed to write file: %v", err)
	}

	log.Printf("Fixed configuration written to %s", path)
}