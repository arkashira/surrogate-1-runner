package correlation

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

// Persistable is an interface for persisting correlation results.
type Persistable interface {
	Save(result CorrelationResult) error
}

// FilePersistor writes JSON files into a directory.
type FilePersistor struct {
	Dir string
}

// Save writes the result as a prettified JSON file named
// correlation-<unix‑nanoseconds>.json inside fp.Dir.
func (fp *FilePersistor) Save(result CorrelationResult) error {
	if fp.Dir == "" {
		return fmt.Errorf("persistor directory not set")
	}
	if err := os.MkdirAll(fp.Dir, 0o755); err != nil {
		return err
	}
	filename := filepath.Join(fp.Dir, fmt.Sprintf("correlation-%d.json", result.Timestamp.UnixNano()))
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer f.Close()
	enc := json.NewEncoder(f)
	enc.SetIndent("", "  ")
	return enc.Encode(result)
}