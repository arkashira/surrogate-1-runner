package formatter

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/axentx/surrogate-1/pkg/compliance/model"
)

// MarkdownFormatter generates a markdown report from the given scan results
type MarkdownFormatter struct{}

// NewMarkdownFormatter returns a new instance of the markdown formatter
func NewMarkdownFormatter() *MarkdownFormatter {
	return &MarkdownFormatter{}
}

// Format generates a markdown report from the given scan results
func (f *MarkdownFormatter) Format(results []model.ScanResult) error {
	// Create the output directory
	outputDir := "output"
	err := os.MkdirAll(outputDir, 0755)
	if err != nil {
		return err
	}

	// Generate the markdown report
	for _, result := range results {
		// Create the markdown file
		filePath := filepath.Join(outputDir, fmt.Sprintf("%s.md", result.ResourceID))
		f, err := os.Create(filePath)
		if err != nil {
			return err
		}
		defer f.Close()

		// Write the markdown content
		_, err = f.WriteString(fmt.Sprintf("# Resource %s\n", result.ResourceID))
		if err != nil {
			return err
		}

		_, err = f.WriteString(fmt.Sprintf("## Description\n%s\n\n", result.Description))
		if err != nil {
			return err
		}

		_, err = f.WriteString(fmt.Sprintf("## Remediation Steps\n%s\n\n", result.RemediationSteps))
		if err != nil {
			return err
		}

		// Write the JSON data
		jsonData, err := json.MarshalIndent(result, "", "  ")
		if err != nil {
			return err
		}
		_, err = f.WriteString(string(jsonData))
		if err != nil {
			return err
		}
	}

	return nil
}