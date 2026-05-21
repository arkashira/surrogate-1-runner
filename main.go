package main

import (
	"opt/axentx/surrogate-1/cli"
	"os"
)

func main() {
	outputDir, validate, err := cli.ParseFlags()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing flags: %v\n", err)
		os.Exit(1)
	}
	
	cli.RunCLI(validate, outputDir)
}