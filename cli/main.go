package main

import (
	"context"
	"fmt"
	"log"
	"os/exec"

	"github.com/spf13/cobra"
)

func main() {
	cmd := flags.NewFlags()

	cmd.Run = func(cmd *cobra.Command, args []string) {
		validate, _ := cmd.Flags().GetBool("validate")
		if validate {
			err := validateCode()
			if err != nil {
				log.Fatal(err)
			}
			fmt.Println("Validation passed.")
		}
		// Existing code generation logic here
	}

	if err := cmd.Execute(); err != nil {
		log.Fatal(err)
	}
}

func validateCode() error {
	cmd := exec.Command("trivy", "image", "your-image-name")
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println(string(output))
		return err
	}
	return nil
}