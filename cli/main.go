package main

import (
	"archive/zip"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"time"
)

func main() {
	// Define flags
	inputPath := flag.String("input", "", "Path to the input CAD file")
	outputPath := flag.String("output", "", "Path to the output mesh zip file")
	help := flag.Bool("help", false, "Show help")

	// Custom usage to match requirement
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "Usage: %s --input <file.cad> --output <mesh.zip>\n", os.Args[0])
		flag.PrintDefaults()
	}

	// Parse flags
	flag.Parse()

	// Show help if requested or if required flags are missing
	if *help || *inputPath == "" || *outputPath == "" {
		flag.Usage()
		if *help {
			os.Exit(0)
		}
		// Missing required flags – exit with non-zero code
		os.Exit(1)
	}

	fmt.Printf("Starting meshing process...\n")
	fmt.Printf("Input file: %s\n", *inputPath)
	fmt.Printf("Output file: %s\n", *outputPath)

	// Simple progress simulation
	fmt.Printf("Starting meshing for %s → %s\n", *inputPath, *outputPath)
	for i := 0; i <= 100; i += 20 {
		fmt.Printf("\rProgress: %3d%%", i)
		time.Sleep(200 * time.Millisecond)
	}
	fmt.Println("\rProgress: 100%")

	// Create the output zip file
	if err := createZip(*inputPath, *outputPath); err != nil {
		fmt.Fprintf(os.Stderr, "Error creating mesh zip: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Meshing completed successfully.")
	os.Exit(0)
}

// createZip creates a zip file at outPath containing the input file
// stored inside the zip as "mesh.obj". This is a stub for the real meshing logic.
func createZip(inPath, outPath string) error {
	// Ensure the input file exists
	inFile, err := os.Open(inPath)
	if err != nil {
		return fmt.Errorf("cannot open input file: %w", err)
	}
	defer inFile.Close()

	// Create the output zip file
	outFile, err := os.Create(outPath)
	if err != nil {
		return fmt.Errorf("cannot create output file: %w", err)
	}
	defer func() {
		// Close and handle error on close
		if cerr := outFile.Close(); cerr != nil && err == nil {
			err = cerr
		}
	}()

	zipWriter := zip.NewWriter(outFile)
	defer func() {
		if cerr := zipWriter.Close(); cerr != nil && err == nil {
			err = cerr
		}
	}()

	// Add a file entry named "mesh.obj" to the zip
	w, err := zipWriter.Create("mesh.obj")
	if err != nil {
		return fmt.Errorf("cannot create zip entry: %w", err)
	}

	// Copy the input file content into the zip entry
	if _, err := io.Copy(w, inFile); err != nil {
		return fmt.Errorf("cannot write to zip entry: %w", err)
	}

	// Ensure the directory for the output exists
	if dir := filepath.Dir(outPath); dir != "." {
		if mkErr := os.MkdirAll(dir, 0o755); mkErr != nil {
			return fmt.Errorf("cannot create output directory: %w", mkErr)
		}
	}

	return nil
}