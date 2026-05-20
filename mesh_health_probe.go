package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

type HealthProbe struct {
	Status  string `json:"status"`
	Message string `json:"message"`
	Details struct {
		MeshFileExists bool   `json:"mesh_file_exists"`
		ResolvedPath   string `json:"resolved_path,omitempty"`
	} `json:"details"`
}

func main() {
	meshFile := "mesh.json"
	resolvedPath, err := filepath.Abs(meshFile)
	if err != nil {
		probe := HealthProbe{
			Status:  "failed",
			Message: "Failed to resolve mesh file path",
			Details: struct {
				MeshFileExists bool   `json:"mesh_file_exists"`
				ResolvedPath   string `json:"resolved_path,omitempty"`
			}{
				MeshFileExists: false,
			},
		}
		outputJSON(probe)
		return
	}

	_, err = os.Stat(meshFile)
	if err != nil {
		probe := HealthProbe{
			Status:  "failed",
			Message: "Mesh file does not exist",
			Details: struct {
				MeshFileExists bool   `json:"mesh_file_exists"`
				ResolvedPath   string `json:"resolved_path,omitempty"`
			}{
				MeshFileExists: false,
				ResolvedPath:   resolvedPath,
			},
		}
		outputJSON(probe)
		return
	}

	probe := HealthProbe{
		Status:  "success",
		Message: "Mesh file exists and path is resolved",
		Details: struct {
			MeshFileExists bool   `json:"mesh_file_exists"`
			ResolvedPath   string `json:"resolved_path,omitempty"`
		}{
			MeshFileExists: true,
			ResolvedPath:   resolvedPath,
		},
	}
	outputJSON(probe)
}

func outputJSON(probe HealthProbe) {
	jsonData, err := json.Marshal(probe)
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return
	}
	fmt.Println(string(jsonData))
}