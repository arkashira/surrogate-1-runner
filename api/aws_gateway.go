package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"gopkg.in/yaml.v3"
)

// ---------------------------------------------------------------------------
// 1️⃣  Configuration types
// ---------------------------------------------------------------------------

// Route defines a mapping from a URL path to a handler name.
type Route struct {
	Path    string `yaml:"path"`
	Handler string `yaml:"handler"`
}

// Config holds all routes loaded from routes.yaml.
type Config struct {
	Routes []Route `yaml:"routes"`
}

// ---------------------------------------------------------------------------
// 2️⃣  Handler registry
// ---------------------------------------------------------------------------

// handlerRegistry maps handler names to actual http.HandlerFunc implementations.
var handlerRegistry = map[string]http.HandlerFunc{
	"s3Handler":    s3Handler,
	"ec2Handler":   ec2Handler,
	"lambdaHandler": lambdaHandler,
}

// ---------------------------------------------------------------------------
// 3️⃣  YAML loading helpers
// ---------------------------------------------------------------------------

// loadConfig reads routes.yaml and unmarshals it into a Config struct.
func loadConfig(path string) (*Config, error) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("reading config file %s: %w", path, err)
	}
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("parsing YAML: %w", err)
	}
	return &cfg, nil
}

// ---------------------------------------------------------------------------
// 4️⃣  Router registration
// ---------------------------------------------------------------------------

// registerRoutes registers all routes from the config to the http.ServeMux.
func registerRoutes(mux *http.ServeMux, cfg *Config) {
	for _, r := range cfg.Routes {
		if handler, ok := handlerRegistry[r.Handler]; ok {
			mux.HandleFunc(r.Path, handler)
			log.Printf("Registered route %s -> %s", r.Path, r.Handler)
		} else {
			log.Printf("⚠️  Handler %s not found for path %s", r.Handler, r.Path)
		}
	}
}

// ---------------------------------------------------------------------------
// 5️⃣  Stub handlers – realistic AWS‑style JSON responses
// ---------------------------------------------------------------------------

func s3Handler(w http.ResponseWriter, r *http.Request) {
	resp := map[string]interface{}{
		"Buckets": []map[string]string{
			{"Name": "example-bucket", "CreationDate": "2023-01-01T00:00:00Z"},
		},
		"Owner": map[string]string{
			"DisplayName": "example-owner",
			"ID":          "1234567890abcdef",
		},
	}
	writeJSON(w, resp)
}

func ec2Handler(w http.ResponseWriter, r *http.Request) {
	resp := map[string]interface{}{
		"Reservations": []map[string]interface{}{
			{
				"Instances": []map[string]interface{}{
					{
						"InstanceId":   "i-0123456789abcdef0",
						"InstanceType": "t2.micro",
						"State": map[string]string{
							"Name": "running",
						},
					},
				},
			},
		},
	}
	writeJSON(w, resp)
}

func lambdaHandler(w http.ResponseWriter, r *http.Request) {
	resp := map[string]interface{}{
		"Functions": []map[string]string{
			{
				"FunctionName": "example-function",
				"Runtime":      "go1.x",
				"Handler":      "main",
			},
		},
	}
	writeJSON(w, resp)
}

// ---------------------------------------------------------------------------
// 6️⃣  Utility – JSON writer
// ---------------------------------------------------------------------------

func writeJSON(w http.ResponseWriter, payload interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(payload); err != nil {
		log.Printf("Error encoding JSON response: %v", err)
	}
}

// ---------------------------------------------------------------------------
// 7️⃣  Main entry point
// ---------------------------------------------------------------------------

func main() {
	// 7.1  Determine config path
	cfgPath := os.Getenv("ROUTES_CONFIG")
	if cfgPath == "" {
		cfgPath = "./config/routes.yaml"
	}

	// 7.2  Load configuration
	cfg, err := loadConfig(cfgPath)
	if err != nil {
		log.Fatalf("Failed to load routes config: %v", err)
	}

	// 7.3  Register routes
	mux := http.NewServeMux()
	registerRoutes(mux, cfg)

	// 7.4  Start HTTP server
	addr := ":8080"
	log.Printf("AWS‑compatible gateway listening on %s", addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}