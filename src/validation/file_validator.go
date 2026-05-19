package validation

import (
	"fmt"
	"os"
)

// ValidateMeshFile checks that the provided mesh file path exists.
// It accepts both absolute and relative paths. If the file does not
// exist, an error is returned with a clear message. If the file exists,
// nil is returned and the workflow can proceed.
func ValidateMeshFile(meshPath string) error {
	if meshPath == "" {
		return fmt.Errorf("mesh file path is empty")
	}

	info, err := os.Stat(meshPath)
	if err != nil {
		if os.IsNotExist(err) {
			return fmt.Errorf("mesh file does not exist: %s", meshPath)
		}
		return fmt.Errorf("error accessing mesh file %s: %w", meshPath, err)
	}

	if info.IsDir() {
		return fmt.Errorf("mesh file path is a directory, not a file: %s", meshPath)
	}

	return nil
}