package cli

import (
	"github.com/spf13/cobra"
)

// NewRootCmd creates the top‑level command that groups all sub‑commands.
func NewRootCmd() *cobra.Command {
	root := &cobra.Command{
		Use:   "surrogate-1",
		Short: "Surrogate‑1 – drift‑detection helper for CI/CD pipelines",
	}

	// Register sub‑commands
	root.AddCommand(NewCICmd())
	// Future commands (e.g. `status`, `report`) can be added here.

	return root
}