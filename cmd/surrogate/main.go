package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"

	"opt/axentx/surrogate-1/pkg/compliance"
)

func main() {
	rootCmd := &cobra.Command{
		Use:   "surrogate",
		Short: "Surrogate CLI",
	}

	scanCmd := &cobra.Command{
		Use:   "scan",
		Short: "Run a compliance scan",
		Run: func(cmd *cobra.Command, args []string) {
			scan, err := compliance.NewScanner()
			if err != nil {
				log.Fatal(err)
			}

			results, err := scan.Scan(context.Background())
			if err != nil {
				log.Fatal(err)
			}

			for _, result := range results {
				fmt.Printf("Rule ID: %s, Severity: %s, Affected Resource: %s\n", result.RuleID, result.Severity, result.AffectedResource)
			}
		},
	}

	rootCmd.AddCommand(scanCmd)

	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}