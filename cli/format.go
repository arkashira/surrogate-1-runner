package cli

import (
	"flag"
	"path/filepath"
)

func ParseFlags() (string, bool, error) {
	var outputDir string
	var validate bool
	
	flag.BoolVar(&validate, "validate", false, "Run security validation on generated code")
	flag.StringVar(&outputDir, "output", "./gen-code", "Output directory for generated code")
	flag.Parse()
	
	// Ensure output directory exists
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return "", false, fmt.Errorf("failed to create output directory: %w", err)
	}
	
	return outputDir, validate, nil
}