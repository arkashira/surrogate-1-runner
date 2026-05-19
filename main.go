package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"/opt/axentx/surrogate-1/validate"
)

var (
	validateFlag = flag.Bool("validate", true, "run security validation on generated code")
	outputDir    = flag.String("output", "", "directory where code is generated")
)

func main() {
	flag.Parse()

	// Validate required parameters
	if *outputDir == "" {
		log.Fatal("--output must specify generated code directory")
	}

	absOutput, err := filepath.Abs(*outputDir)
	if err != nil {
		log.Fatalf("failed to resolve output path: %v", err)
	}

	// Load configuration
	config := validate.DefaultConfig()

	// Run security scan if enabled
	if config.EnableSecurityScan {
		fmt.Printf("🔍 Running security scan on %s...\n", absOutput)

		pass, output, err := validate.SecurityScan(absOutput)
		if err != nil {
			log.Fatalf("validation error: %v", err)
		}

		fmt.Print(output) // Print Trivy results

		if pass {
			fmt.Println("✅ Security scan passed")
		} else {
			fmt.Println("❌ Security scan failed - critical vulnerabilities detected")
			os.Exit(1) // Exit with error code on failure
		}
	}
}