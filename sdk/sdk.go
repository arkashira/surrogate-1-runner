package sdk

import (
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
)

// Mesh takes an input path and an output path, and runs the meshing engine
// on the input file, writing the output to the specified output path.
// If the meshing engine is not available, it falls back to copying the input file.
func Mesh(inputPath, outputPath string) error {
	// Ensure the input file exists
	if _, err := os.Stat(inputPath); os.IsNotExist(err) {
		return fmt.Errorf("input file does not exist: %s", inputPath)
	}

	// Get the absolute paths
	absInputPath, err := filepath.Abs(inputPath)
	if err!= nil {
		return fmt.Errorf("failed to get absolute path for input: %v", err)
	}

	absOutputPath, err := filepath.Abs(outputPath)
	if err!= nil {
		return fmt.Errorf("failed to get absolute path for output: %v", err)
	}

	// Try to run the meshing engine command
	cmd := exec.Command("meshing-engine", "--input", absInputPath, "--output", absOutputPath)
	err = cmd.Run()
	if err!= nil {
		// Fallback to copying the input file if the meshing engine fails
		return copyFile(absInputPath, absOutputPath)
	}

	return nil
}

// copyFile copies the contents of the source file to the destination file.
func copyFile(src, dst string) error {
	// Open the source file.
	in, err := os.Open(src)
	if err!= nil {
		return err
	}
	defer in.Close()

	// Ensure the destination directory exists.
	if err := os.MkdirAll(getDir(dst), 0755); err!= nil {
		return err
	}

	// Create the destination file.
	out, err := os.Create(dst)
	if err!= nil {
		return err
	}
	defer func() {
		// Ensure the file is closed even on copy error.
		cerr := out.Close()
		if err == nil && cerr!= nil {
			err = cerr
		}
	}()

	// Copy contents.
	_, err = io.Copy(out, in)
	return err
}

// getDir returns the directory component of a path.
func getDir(path string) string {
	dir, _ := os.Split(path)
	return dir
}