package fd

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
)

// FDInfo mirrors the protobuf FDInfo message.
type FDInfo struct {
	FD     uint32
	Target string
	Type   string
}

// ListOpenFDs enumerates the current process's open file descriptors
// by reading /proc/self/fd. It returns a slice of FDInfo structs.
func ListOpenFDs() ([]FDInfo, error) {
	const procFdPath = "/proc/self/fd"
	entries, err := os.ReadDir(procFdPath)
	if err != nil {
		return nil, fmt.Errorf("reading %s: %w", procFdPath, err)
	}

	var infos []FDInfo
	for _, entry := range entries {
		// The directory entry name is the FD number.
		fdNum, err := parseFD(entry.Name())
		if err != nil {
			// Skip entries that aren't numeric.
			continue
		}

		linkPath := filepath.Join(procFdPath, entry.Name())
		target, err := os.Readlink(linkPath)
		if err != nil {
			// If we cannot read the link, still record the FD with an error marker.
			target = fmt.Sprintf("unreadable: %v", err)
		}

		fdType := inferFDType(target)

		infos = append(infos, FDInfo{
			FD:     fdNum,
			Target: target,
			Type:   fdType,
		})
	}
	return infos, nil
}

// parseFD converts a directory entry name to a uint32 FD number.
func parseFD(name string) (uint32, error) {
	var fd uint32
	_, err := fmt.Sscanf(name, "%d", &fd)
	return fd, err
}

// inferFDType provides a best‑effort classification of the FD based on its target string.
func inferFDType(target string) string {
	switch {
	case strings.HasPrefix(target, "socket:"):
		return "socket"
	case strings.HasPrefix(target, "pipe:"):
		return "pipe"
	case strings.HasPrefix(target, "/"):
		return "file"
	default:
		return "unknown"
	}
}

// Ensure the package compiles even when the OS does not expose /proc (e.g., Windows).
func init() {
	if _, err := os.Stat("/proc/self/fd"); err != nil && !os.IsNotExist(err) {
		// No action needed; ListOpenFDs will return an error at call time.
	}
}