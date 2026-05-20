package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// HealthProbeResponse represents the standardized JSON output for health probes
type HealthProbeResponse struct {
	Status    string `json:"status"`
	CheckedAt string `json:"checked_at"`
	Details   struct {
		MeshFileExists bool   `json:"mesh_file_exists"`
		ResolvedPath   string `json:"resolved_path,omitempty"`
		ErrorMessage   string `json:"error_message,omitempty"`
	} `json:"details"`
}

// MeshConfig holds the mesh file configuration
type MeshConfig struct {
	MeshFilePath string `json:"mesh_file_path"`
}

// LoadMeshConfig loads mesh configuration from environment or defaults
func LoadMeshConfig() (*MeshConfig, error) {
	meshPath := os.Getenv("MESH_FILE_PATH")
	if meshPath == "" {
		meshPath = "/opt/axentx/surrogate-1/mesh.json"
	}
	return &MeshConfig{
		MeshFilePath: meshPath,
	}, nil
}

// ResolvePath resolves the mesh file path to an absolute path
func ResolvePath(meshPath string) (string, error) {
	absPath, err := filepath.Abs(meshPath)
	if err != nil {
		return "", fmt.Errorf("failed to resolve absolute path: %w", err)
	}
	return absPath, nil
}

// ValidateMeshFile checks if the mesh file exists and is accessible
func ValidateMeshFile(meshPath string) (bool, string, error) {
	absPath, err := ResolvePath(meshPath)
	if err != nil {
		return false, "", fmt.Errorf("path resolution failed: %w", err)
	}

	// Check if file exists
	if _, err := os.Stat(absPath); os.IsNotExist(err) {
		return false, absPath, fmt.Errorf("mesh file does not exist: %s", absPath)
	}

	// Check if file is readable
	if err := os.Rewind(absPath); err != nil {
		return false, absPath, fmt.Errorf("mesh file is not readable: %w", err)
	}

	return true, absPath, nil
}

// HealthProbeHandler handles HTTP health probe requests
func HealthProbeHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	meshConfig, err := LoadMeshConfig()
	if err != nil {
		writeHealthProbeFailure(w, "failed to load mesh config", err.Error())
		return
	}

	exists, resolvedPath, err := ValidateMeshFile(meshConfig.MeshFilePath)
	if err != nil {
		writeHealthProbeFailure(w, "mesh file validation failed", err.Error())
		return
	}

	response := HealthProbeResponse{
		Status:    "healthy",
		CheckedAt: time.Now().UTC().Format(time.RFC3339),
		Details: struct {
			MeshFileExists bool   `json:"mesh_file_exists"`
			ResolvedPath   string `json:"resolved_path,omitempty"`
			ErrorMessage   string `json:"error_message,omitempty"`
		}{
			MeshFileExists: exists,
			ResolvedPath:   resolvedPath,
		},
	}

	if !exists {
		response.Status = "unhealthy"
		response.Details.ErrorMessage = "mesh file not found or path not resolved"
	}

	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("failed to encode health probe response: %v", err)
	}
}

// writeHealthProbeFailure writes a failure response in standardized JSON format
func writeHealthProbeFailure(w http.ResponseWriter, message, errMessage string) {
	response := HealthProbeResponse{
		Status:    "unhealthy",
		CheckedAt: time.Now().UTC().Format(time.RFC3339),
		Details: struct {
			MeshFileExists bool   `json:"mesh_file_exists"`
			ResolvedPath   string `json:"resolved_path,omitempty"`
			ErrorMessage   string `json:"error_message,omitempty"`
		}{
			MeshFileExists: false,
			ErrorMessage:   errMessage,
		},
	}

	w.WriteHeader(http.StatusServiceUnavailable)
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("failed to encode health probe failure response: %v", err)
	}
}

// SetupHealthProbeRoutes configures the HTTP routes for health probing
func SetupHealthProbeRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/health", HealthProbeHandler)
	mux.HandleFunc("/healthz", HealthProbeHandler)
	mux.HandleFunc("/ready", HealthProbeHandler)
}

// Main entry point for the health probe service
func main() {
	mux := http.NewServeMux()
	SetupHealthProbeRoutes(mux)

	port := os.Getenv("HEALTH_PROBE_PORT")
	if port == "" {
		port = "8080"
	}

	addr := fmt.Sprintf(":%s", port)
	log.Printf("Starting health probe server on %s", addr)

	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("failed to start health probe server: %v", err)
	}
}