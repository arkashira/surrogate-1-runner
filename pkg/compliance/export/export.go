package export

import (
	"fmt"
	"log"
	"os"

	"github.com/axentx/surrogate-1/pkg/compliance/model"
)

// Exporter exports the scan results to a file
type Exporter struct{}

// NewExporter returns a new instance of the exporter
func NewExporter() *Exporter {
	return &Exporter{}
}

// Export exports the scan results to a file
func (e *Exporter) Export(results []model.ScanResult) error {
	// Create the output file
	outputFile, err := os.Create("output.json")
	if err != nil {
		return err
	}
	defer outputFile.Close()

	// Write the JSON data
	jsonData, err := json.MarshalIndent(results, "", "  ")
	if err != nil {
		return err
	}
	_, err = outputFile.WriteString(string(jsonData))
	if err != nil {
		return err
	}

	return nil
}