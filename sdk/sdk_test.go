package sdk

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
)

func TestMesh(t *testing.T) {
	// Create a temporary directory for testing
	tempDir := t.TempDir()

	// Create a test input file
	inputFile := filepath.Join(tempDir, "input.txt")
	err := ioutil.WriteFile(inputFile, []byte("test input"), 0644)
	if err!= nil {
		t.Fatalf("failed to create test input file: %v", err)
	}

	// Create an output file path
	outputFile := filepath.Join(tempDir, "output.txt")

	// Call the Mesh function
	err = Mesh(inputFile, outputFile)
	if err!= nil {
		t.Fatalf("Mesh function failed: %v", err)
	}

	// Check if the output file was created
	_, err = os.Stat(outputFile)
	if os.IsNotExist(err) {
		t.Fatalf("output file was not created: %s", outputFile)
	}
}

func TestMesh_CopiesFile(t *testing.T) {
	// Create temporary input file.
	tmpDir, err := ioutil.TempDir("", "sdk_test")
	if err!= nil {
		t.Fatalf("temp dir creation failed: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	inputPath := filepath.Join(tmpDir, "input.txt")
	outputPath := filepath.Join(tmpDir, "output.txt")
	content := []byte("mesh test content")

	if err := ioutil.WriteFile(inputPath, content, 0644); err!= nil {
		t.Fatalf("write input failed: %v", err)
	}

	// Run Mesh with a non-existent meshing engine to test the fallback.
	// This can be done by temporarily renaming the meshing engine executable.
	meshingEnginePath := "/path/to/meshing-engine"
	originalName := meshingEnginePath + ".original"
	if err := os.Rename(meshingEnginePath, originalName); err!= nil {
		t.Skip("meshing engine not found, skipping test")
	}
	defer func() {
		if err := os.Rename(originalName, meshingEnginePath); err!= nil {
			t.Errorf("failed to restore meshing engine: %v", err)
		}
	}()

	// Run Mesh.
	if err := Mesh(inputPath, outputPath); err!= nil {
		t.Fatalf("Mesh returned error: %v", err)
	}

	// Verify output.
	got, err := ioutil.ReadFile(outputPath)
	if err!= nil {
		t.Fatalf("read output failed: %v", err)
	}
	if string(got)!= string(content) {
		t.Fatalf("output mismatch: got %q, want %q", string(got), string(content))
	}
}