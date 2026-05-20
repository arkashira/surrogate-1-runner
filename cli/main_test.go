package main

import (
	"bytes"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
)

// ---------------------------------------------------------------------
// Helper: obtain an executable for the CLI.
//
// The test suite can work in two ways:
//
//   1. If the binary already exists (e.g. CI built it), set the
//      environment variable SURROGATE_MESH_BIN to its path.
//   2. Otherwise the helper builds a temporary binary with `go build`.
//
// This gives the speed of re‑using a pre‑built binary while still
// guaranteeing that the code under test is compiled from the current
// checkout.
//
// Returns the path to the executable and a cleanup function that removes
// the temporary binary (a no‑op when SURROGATE_MESH_BIN is used).
// ---------------------------------------------------------------------
func getCLI(t *testing.T) (binPath string, cleanup func()) {
	t.Helper()

	if prebuilt := os.Getenv("SURROGATE_MESH_BIN"); prebuilt != "" {
		if _, err := os.Stat(prebuilt); err != nil {
			t.Fatalf("SURROGATE_MESH_BIN=%s does not exist: %v", prebuilt, err)
		}
		return prebuilt, func() {}
	}

	tmpDir := t.TempDir()
	binPath = filepath.Join(tmpDir, "surrogate-mesh")
	cmd := exec.Command("go", "build", "-o", binPath, ".")
	// Ensure we are building the package that contains main.go.
	// If the test lives in ./cli, the working directory is already correct.
	cmd.Dir = filepath.Dir(".")
	out, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("failed to build CLI binary: %v\noutput: %s", err, string(out))
	}
	return binPath, func() { os.Remove(binPath) }
}

// ---------------------------------------------------------------------
// TestHelp – verifies that the binary prints a usage message and exits
// with status 0 when invoked with `--help`.
// ---------------------------------------------------------------------
func TestHelp(t *testing.T) {
	bin, cleanup := getCLI(t)
	t.Cleanup(cleanup)

	cmd := exec.Command(bin, "--help")
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &out

	if err := cmd.Run(); err != nil {
		t.Fatalf("CLI --help returned error: %v\noutput: %s", err, out.String())
	}

	output := out.String()
	if !(strings.Contains(output, "Usage") || strings.Contains(output, "surrogate-mesh")) {
		t.Fatalf("help output does not contain expected usage information: %s", output)
	}
}

// ---------------------------------------------------------------------
// TestRun – a minimal end‑to‑end execution test.
// It creates a temporary (empty) CAD file, runs the CLI with
// `--input` and `--output`, and checks that the expected zip file is
// produced.  The content of the zip is not validated here – that is a
// separate unit‑test concern – but the existence of the file proves that
// the command line plumbing works.
// ---------------------------------------------------------------------
func TestRun(t *testing.T) {
	bin, cleanup := getCLI(t)
	t.Cleanup(cleanup)

	// 1️⃣ Create a temporary empty CAD file.
	tmpInput, err := ioutil.TempFile(t.TempDir(), "input-*.cad")
	if err != nil {
		t.Fatalf("failed to create temporary input file: %v", err)
	}
	tmpInput.Close() // the CLI only needs a path, not an open handle.

	// 2️⃣ Define where the output zip should be written.
	tmpOutput := filepath.Join(t.TempDir(), "mesh.zip")

	// 3️⃣ Execute the CLI.
	cmd := exec.Command(bin,
		"--input", tmpInput.Name(),
		"--output", tmpOutput,
	)
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &out

	if err := cmd.Run(); err != nil {
		t.Fatalf("CLI execution failed: %v\noutput: %s", err, out.String())
	}

	// 4️⃣ Verify that the output file exists.
	if _, err := os.Stat(tmpOutput); os.IsNotExist(err) {
		t.Fatalf("expected output file %s to exist, but it does not", tmpOutput)
	}
}

// ---------------------------------------------------------------------
// TestInvalidFlags – ensures the program fails (non‑zero exit status)
// when required flags are omitted.  This guards against silent success
// that could hide user‑error handling bugs.
// ---------------------------------------------------------------------
func TestInvalidFlags(t *testing.T) {
	bin, cleanup := getCLI(t)
	t.Cleanup(cleanup)

	cmd := exec.Command(bin) // no flags at all
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &out

	err := cmd.Run()
	if err == nil {
		t.Fatalf("expected non‑zero exit code when required flags are missing, got success")
	}
}