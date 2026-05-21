package fdscout

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
)

// OpenFD represents a single open file descriptor of the current process.
type OpenFD struct {
	// FD is the numeric file descriptor (e.g., 0, 1, 2, ...).
	FD int
	// Target is the path that the descriptor points to, as reported by /proc/self/fd/<fd>.
	Target string
}

// FDListError is a typed error returned by ListOpenFDs.
type FDListError struct {
	Op  string // operation being performed, e.g., "read /proc/self/fd"
	Err error  // underlying error
}

// Error implements the error interface.
func (e *FDListError) Error() string {
	return fmt.Sprintf("fdscout: %s: %v", e.Op, e.Err)
}

// Unwrap returns the underlying error.
func (e *FDListError) Unwrap() error { return e.Err }

// ListOpenFDs returns a slice of OpenFD structs describing the current
// process's open file descriptors. It reads the /proc/self/fd directory
// using os.ReadDir and resolves each entry via os.Readlink.
//
// The function does not require elevated privileges and works inside
// OCI sandboxes (Docker, Firecracker, Kata). Errors are wrapped in FDListError.
func ListOpenFDs() ([]OpenFD, error) {
	const procFDPath = "/proc/self/fd"

	entries, err := os.ReadDir(procFDPath)
	if err != nil {
		return nil, &FDListError{Op: "read /proc/self/fd", Err: err}
	}

	fds := make([]OpenFD, 0, len(entries))
	for _, entry := range entries {
		name := entry.Name()
		fdNum, err := strconv.Atoi(name)
		if err != nil {
			// Skip non-numeric entries (should not happen in /proc/self/fd)
			continue
		}

		linkPath := filepath.Join(procFDPath, name)
		target, err := os.Readlink(linkPath)
		if err != nil {
			// If we cannot resolve the link, wrap and return the error.
			return nil, &FDListError{Op: fmt.Sprintf("readlink %s", linkPath), Err: err}
		}

		fds = append(fds, OpenFD{
			FD:     fdNum,
			Target: target,
		})
	}

	return fds, nil
}