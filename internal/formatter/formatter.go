package formatter

import (
	"bytes"
	"fmt"
	"log"
	"os/exec"
	"path/filepath"
	"strings"
)

// Formatter formats files based on their extension using external tools.
type Formatter struct {
	// extMap maps a file extension (lower‑case, including the dot) to the
	// command and its arguments (excluding the file path, which is appended
	// automatically).
	extMap map[string][]string
	logger *log.Logger
}

// NewFormatter creates a Formatter with the default extension‑to‑command mapping.
// The provided logger is used for warnings; if nil, a no‑op logger is used.
func NewFormatter(logger *log.Logger) *Formatter {
	if logger == nil {
		logger = log.New(&bytes.Buffer{}, "", 0)
	}
	return &Formatter{
		extMap: defaultExtMap(),
		logger: logger,
	}
}

// defaultExtMap returns the built‑in mapping of extensions to formatter commands.
func defaultExtMap() map[string][]string {
	return map[string][]string{
		".go":   {"gofmt", "-w"},
		".py":   {"black"},
		".js":   {"prettier", "--write"},
		".ts":   {"prettier", "--write"},
		".json": {"prettier", "--write"},
		".css": {"prettier", "--write"},
		".html": {"prettier", "--write"},
	}
}

// FormatFile detects the language of the given file by its extension and runs the
// appropriate formatter. Unsupported extensions are skipped with a warning.
// Formatter errors are returned to the caller.
func (f *Formatter) FormatFile(path string) error {
	ext := strings.ToLower(filepath.Ext(path))
	cmdArgs, ok := f.extMap[ext]
	if !ok {
		f.logger.Printf("warning: no formatter configured for extension %s, skipping %s", ext, path)
		return nil
	}

	// Append the file path to the command arguments.
	fullArgs := append(cmdArgs[1:], path)
	cmd := exec.Command(cmdArgs[0], fullArgs...)

	var stderr bytes.Buffer
	cmd.Stderr = &stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("formatter %s failed on %s: %w: %s", cmdArgs[0], path, err, strings.TrimSpace(stderr.String()))
	}
	return nil
}