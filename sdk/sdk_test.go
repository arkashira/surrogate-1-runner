package sdk

import (
	"os"
	"path/filepath"
	"testing"
)

// TestMesh validates that Mesh creates a non‑empty output file when given a
// valid input file. All files are written to a temporary directory that is
// removed after the test finishes.
func TestMesh(t *testing.T) {
	// --------------------------------------------------------------------
	// 1️⃣  Set up an isolated temporary workspace
	// --------------------------------------------------------------------
	tmpDir, err := os.MkdirTemp("", "sdk_test_*")
	if err != nil {
		t.Fatalf("failed to create temporary directory: %v", err)
	}
	// Ensure the directory is removed no matter how the test exits.
	defer os.RemoveAll(tmpDir)

	// --------------------------------------------------------------------
	// 2️⃣  Prepare a deterministic input file
	// --------------------------------------------------------------------
	const inputData = "test data for meshing"
	inputPath := filepath.Join(tmpDir, "input.txt")
	if err := os.WriteFile(inputPath, []byte(inputData), 0o600); err != nil {
		t.Fatalf("failed to write input file %s: %v", inputPath, err)
	}

	// --------------------------------------------------------------------
	// 3️⃣  Define where Mesh should write its result
	// --------------------------------------------------------------------
	outputPath := filepath.Join(tmpDir, "output.txt")

	// --------------------------------------------------------------------
	// 4️⃣  Execute the function under test
	// --------------------------------------------------------------------
	if err := Mesh(inputPath, outputPath); err != nil {
		t.Fatalf("Mesh returned an unexpected error: %v", err)
	}

	// --------------------------------------------------------------------
	// 5️⃣  Verify the output file exists
	// --------------------------------------------------------------------
	if _, err := os.Stat(outputPath); os.IsNotExist(err) {
		t.Fatalf("expected output file %s to exist, but it does not", outputPath)
	} else if err != nil {
		t.Fatalf("error checking output file %s: %v", outputPath, err)
	}

	// --------------------------------------------------------------------
	// 6️⃣  Verify the output file is not empty (extra safety)
	// --------------------------------------------------------------------
	data, err := os.ReadFile(outputPath)
	if err != nil {
		t.Fatalf("failed to read output file %s: %v", outputPath, err)
	}
	if len(data) == 0 {
		t.Fatalf("output file %s is empty; Mesh should produce data", outputPath)
	}
}