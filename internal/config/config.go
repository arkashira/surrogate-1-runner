package config

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/axentx/surrogate-1/internal/report"
)

func GetReportConfig() (*report.ReportConfig, error) {
	reportConfig := &report.ReportConfig{}

	// Assuming reportConfig is defined in the report package
	// and has fields for report output path, log path, etc.

	return reportConfig, nil
}